from __future__ import annotations

import argparse
import base64
import ctypes
import hashlib
import json
import os
import platform
import struct
import sys
import tempfile
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen


REQUEST_FILE_NAME = 0x00000001
REQUEST_PATH = 0x00000002
SDK_SHA256 = {
    "Everything32.dll": "C28CD066AF36CAE4403A9933847AFF01DB928787D86751F014A1FA60D8B97FDA",
    "Everything64.dll": "C7AB8B47F7DD4C41AA735F4BA40B35AD5460A86FA7ABE0C94383F12BCE33BFB6",
    "EverythingARM.dll": "11620A496539BC63C62985CDF0079B757F7988CF3CBDF465CD97940A081700A3",
    "EverythingARM64.dll": "8531EA393677DD8FD37BED7420AC93344CD458B9A1324BA65C4A75D024D61886",
}


class EverythingQueryError(RuntimeError):
    def __init__(self, code: int, detail: str):
        super().__init__(f"Everything 查询失败，错误码 {code}: {detail}")
        self.code = code


def python_bits() -> int:
    return struct.calcsize("P") * 8


def sdk_dll_name() -> str:
    machine = platform.machine().lower()
    if "arm" in machine or "aarch" in machine:
        return "EverythingARM64.dll" if python_bits() == 64 else "EverythingARM.dll"
    return "Everything64.dll" if python_bits() == 64 else "Everything32.dll"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def materialize_bundled_dll() -> Path:
    dll_name = sdk_dll_name()
    expected_hash = SDK_SHA256[dll_name]
    skill_root = Path(__file__).resolve().parent.parent
    payload_path = skill_root / "assets" / "everything-sdk" / "payload" / f"{dll_name}.txt"
    if not payload_path.is_file():
        raise FileNotFoundError(f"找不到内置 Everything SDK 载荷: {payload_path}")

    target_dir = Path(tempfile.gettempdir()) / "everything-search-sdk" / expected_hash[:16].lower()
    target_path = target_dir / dll_name
    if target_path.is_file() and sha256_file(target_path) == expected_hash:
        return target_path

    try:
        payload = base64.b64decode(payload_path.read_text(encoding="ascii"), validate=True)
    except (OSError, ValueError) as exc:
        raise RuntimeError(f"无法解码内置 Everything SDK 载荷: {payload_path}") from exc
    actual_hash = hashlib.sha256(payload).hexdigest().upper()
    if actual_hash != expected_hash:
        raise RuntimeError(
            f"内置 Everything SDK 载荷校验失败: {dll_name}，"
            f"期望 {expected_hash}，实际 {actual_hash}"
        )

    target_dir.mkdir(parents=True, exist_ok=True)
    temporary_path = target_dir / f"{dll_name}.{os.getpid()}.tmp"
    temporary_path.write_bytes(payload)
    os.replace(temporary_path, target_path)
    if sha256_file(target_path) != expected_hash:
        raise RuntimeError(f"释放后的 Everything SDK DLL 校验失败: {target_path}")
    return target_path


def candidate_dlls() -> list[Path]:
    dll_name = sdk_dll_name()
    candidates = []
    configured = os.environ.get("EVERYTHING_SDK_DLL")
    if configured:
        candidates.append(Path(configured).expanduser())
    candidates.extend(
        [
            Path(__file__).resolve().parent / dll_name,
            Path.cwd() / dll_name,
            Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Everything" / dll_name,
        ]
    )
    return candidates


def resolve_dll(explicit: str | None) -> Path:
    if explicit:
        path = Path(explicit).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(f"找不到指定的 Everything SDK DLL: {path}")
        return path
    configured = os.environ.get("EVERYTHING_SDK_DLL")
    if configured:
        path = Path(configured).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(f"EVERYTHING_SDK_DLL 指向的文件不存在: {path}")
        return path
    try:
        return materialize_bundled_dll()
    except FileNotFoundError:
        pass
    checked = []
    for path in candidate_dlls():
        resolved = path.resolve()
        checked.append(str(resolved))
        if resolved.is_file():
            return resolved
    details = "\n".join(f"- {path}" for path in checked)
    raise FileNotFoundError(
        f"找不到与当前 Python 架构匹配的 {sdk_dll_name()}。已检查:\n{details}\n"
        "请通过 --dll 指定可信 DLL，或设置 EVERYTHING_SDK_DLL。"
    )


class EverythingClient:
    def __init__(self, dll_path: Path):
        try:
            self.dll = ctypes.WinDLL(str(dll_path))
        except OSError as exc:
            raise RuntimeError(
                f"无法加载 DLL: {dll_path}。请确认 DLL 与 {python_bits()} 位 Python 匹配。原始错误: {exc}"
            ) from exc
        self.dll_path = dll_path
        self._bind()

    def _bind(self) -> None:
        self.dll.Everything_SetSearchW.argtypes = [ctypes.c_wchar_p]
        self.dll.Everything_SetSearchW.restype = None
        self.dll.Everything_SetMax.argtypes = [ctypes.c_uint32]
        self.dll.Everything_SetMax.restype = None
        self.dll.Everything_SetOffset.argtypes = [ctypes.c_uint32]
        self.dll.Everything_SetOffset.restype = None
        self.dll.Everything_SetRequestFlags.argtypes = [ctypes.c_uint32]
        self.dll.Everything_SetRequestFlags.restype = None
        self.dll.Everything_QueryW.argtypes = [ctypes.c_bool]
        self.dll.Everything_QueryW.restype = ctypes.c_bool
        self.dll.Everything_GetNumResults.argtypes = []
        self.dll.Everything_GetNumResults.restype = ctypes.c_uint32
        self.dll.Everything_GetResultFullPathNameW.argtypes = [
            ctypes.c_uint32,
            ctypes.POINTER(ctypes.c_wchar),
            ctypes.c_uint32,
        ]
        self.dll.Everything_GetResultFullPathNameW.restype = ctypes.c_uint32
        self.dll.Everything_IsFolderResult.argtypes = [ctypes.c_uint32]
        self.dll.Everything_IsFolderResult.restype = ctypes.c_bool
        self.dll.Everything_GetLastError.argtypes = []
        self.dll.Everything_GetLastError.restype = ctypes.c_uint32
        self.dll.Everything_Reset.argtypes = []
        self.dll.Everything_Reset.restype = None
        self.dll.Everything_CleanUp.argtypes = []
        self.dll.Everything_CleanUp.restype = None

    def search(self, query: str, limit: int, offset: int) -> list[dict[str, str]]:
        self.dll.Everything_Reset()
        self.dll.Everything_SetSearchW(query)
        self.dll.Everything_SetMax(limit)
        self.dll.Everything_SetOffset(offset)
        self.dll.Everything_SetRequestFlags(REQUEST_FILE_NAME | REQUEST_PATH)
        if not self.dll.Everything_QueryW(True):
            code = int(self.dll.Everything_GetLastError())
            errors = {
                1: "内存不足",
                2: "Everything IPC 不可用",
                3: "无法注册查询窗口类",
                4: "无法创建查询窗口",
                5: "无法创建查询线程",
                6: "结果索引无效",
                7: "调用顺序无效",
            }
            detail = errors.get(code, "未知错误")
            raise EverythingQueryError(code, detail)
        results = []
        for index in range(int(self.dll.Everything_GetNumResults())):
            buffer = ctypes.create_unicode_buffer(32768)
            self.dll.Everything_GetResultFullPathNameW(index, buffer, len(buffer))
            results.append(
                {
                    "path": buffer.value,
                    "type": "folder" if self.dll.Everything_IsFolderResult(index) else "file",
                }
            )
        return results

    def close(self) -> None:
        self.dll.Everything_CleanUp()


def build_query(query: str, result_type: str) -> str:
    if result_type == "folder":
        return f"folder: {query}"
    if result_type == "file":
        return f"file: {query}"
    return query


def everything_ini_candidates() -> list[Path]:
    candidates = []
    app_data = os.environ.get("APPDATA")
    program_files = os.environ.get("ProgramFiles")
    if app_data:
        candidates.append(Path(app_data) / "Everything" / "Everything.ini")
    if program_files:
        candidates.append(Path(program_files) / "Everything" / "Everything.ini")
    return candidates


def read_ini_value(key: str) -> str | None:
    prefix = f"{key.lower()}="
    for path in everything_ini_candidates():
        if not path.is_file():
            continue
        try:
            for line in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
                if line.lower().startswith(prefix):
                    return line.split("=", 1)[1].strip()
        except OSError:
            continue
    return None


def resolve_http_url(explicit: str | None) -> str:
    configured = explicit or os.environ.get("EVERYTHING_HTTP_URL")
    if configured:
        url = configured
    else:
        port_text = read_ini_value("http_server_port") or "80"
        try:
            port = int(port_text)
        except ValueError as exc:
            raise RuntimeError(f"Everything HTTP 端口无效: {port_text}") from exc
        if not 1 <= port <= 65535:
            raise RuntimeError(f"Everything HTTP 端口超出范围: {port}")
        url = f"http://127.0.0.1:{port}/"

    parsed = urlparse(url)
    if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise RuntimeError("Everything HTTP 地址必须使用本机 http://127.0.0.1、localhost 或 ::1")
    return url.rstrip("/") + "/"


def search_http(
    base_url: str,
    query: str,
    limit: int,
    offset: int,
    timeout: float,
) -> list[dict[str, str]]:
    parameters = urlencode(
        {
            "search": query,
            "offset": offset,
            "count": limit,
            "json": 1,
            "path_column": 1,
        }
    )
    request = Request(f"{base_url}?{parameters}", headers={"Accept": "application/json"})
    try:
        with urlopen(request, timeout=timeout) as response:
            payload = json.load(response)
    except HTTPError as exc:
        raise RuntimeError(f"Everything HTTP 查询失败，HTTP 状态码 {exc.code}") from exc
    except (URLError, TimeoutError, OSError) as exc:
        raise RuntimeError(f"Everything HTTP 查询不可用: {base_url}，原始错误: {exc}") from exc
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError("Everything HTTP 返回的不是有效 JSON") from exc

    raw_results = payload.get("results")
    if not isinstance(raw_results, list):
        raise RuntimeError("Everything HTTP JSON 缺少 results 数组")

    results = []
    for item in raw_results:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name", ""))
        parent = str(item.get("path", ""))
        full_path = str(Path(parent) / name) if parent else name
        results.append(
            {
                "path": full_path,
                "type": "folder" if item.get("type") == "folder" else "file",
            }
        )
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="通过 Everything SDK 搜索 Windows 本机文件和文件夹")
    parser.add_argument("query", help="Everything 搜索词或完整搜索表达式")
    parser.add_argument("--type", choices=("all", "file", "folder"), default="all", dest="result_type")
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--dll", help="Everything32.dll 或 Everything64.dll 的路径")
    parser.add_argument(
        "--transport",
        choices=("auto", "sdk", "http"),
        default="auto",
        help="查询通道，auto 会在 SDK IPC 错误码 2 时回退到本机 HTTP",
    )
    parser.add_argument("--http-url", help="本机 Everything HTTP 地址，例如 http://127.0.0.1:22080/")
    parser.add_argument("--http-timeout", type=float, default=10.0)
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if os.name != "nt":
        raise RuntimeError("everything-search 仅支持 Windows，当前系统无法调用 Everything SDK IPC。")
    if args.limit < 1:
        raise ValueError("--limit 必须大于 0")
    if args.offset < 0:
        raise ValueError("--offset 不能小于 0")
    if args.http_timeout <= 0:
        raise ValueError("--http-timeout 必须大于 0")

    query = build_query(args.query, args.result_type)
    if args.transport == "http":
        results = search_http(
            resolve_http_url(args.http_url), query, args.limit, args.offset, args.http_timeout
        )
    else:
        dll_path = resolve_dll(args.dll)
        client = EverythingClient(dll_path)
        try:
            try:
                results = client.search(query, args.limit, args.offset)
            except EverythingQueryError as exc:
                if args.transport != "auto" or exc.code != 2:
                    raise
                results = search_http(
                    resolve_http_url(args.http_url), query, args.limit, args.offset, args.http_timeout
                )
        finally:
            client.close()
    if args.as_json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for item in results:
            print(item["path"])
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
