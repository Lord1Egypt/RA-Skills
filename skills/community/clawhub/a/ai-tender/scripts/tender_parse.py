import sys
import os
import json
import time
import urllib.request
import urllib.parse
import socket
import subprocess
from contextlib import contextmanager, redirect_stdout, redirect_stderr
from io import StringIO, BytesIO
from pathlib import Path
from typing import Tuple, Dict, Any, List

SCRIPT_DIR = Path(__file__).resolve().parent
PRASE_SKILL_DIR = SCRIPT_DIR.parent
WECHAT_IMAGE_URL = "https://aistatic.supcon.com/tender/assets/jpg/home_link-Dwolmpjc.jpg"
sys.path.insert(0, str(PRASE_SKILL_DIR))

# ========== 内联公共工具 ==========
import re
from datetime import datetime
from typing import Optional


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def safe_json_loads(text: str) -> Dict[str, Any]:
    text = text.strip()
    m = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if m:
        text = m.group(1).strip()
    if text.startswith("{") and text.endswith("}"):
        return json.loads(text)
    m = re.search(r"\{[\s\S]*\}", text)
    if m:
        return json.loads(m.group(0))
    raise ValueError(f"无法解析 JSON，获取内容: {text[:300]}...")


def load_env_config():
    try:
        env_md_path = SCRIPT_DIR / "env_config.md"
        if not env_md_path.exists():
            return
        with env_md_path.open("r", encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = value
    except Exception:
        pass


class LLMClient:
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        load_env_config()
        self.api_key = api_key or os.environ.get("LLM_API_KEY")
        self.base_url = base_url or os.environ.get("LLM_BASE_URL")
        if not self.api_key:
            raise ValueError("LLM API key is required. Please set LLM_API_KEY environment variable or pass api_key parameter.")
        try:
            from openai import OpenAI  # type: ignore
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        except ImportError:
            raise ImportError("OpenAI library is required. Please install it with: pip install openai")

    def chat(
        self,
        user_prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: Optional[int] = 128000,
        **kwargs
    ) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})
        try:
            resolved_model = model or os.environ.get("LLM_MODEL")
            response = _call_with_overload_retry(
                lambda: self.client.chat.completions.create(
                    model=resolved_model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    **kwargs
                ),
                operation_name="chat.completions.create"
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"LLM API call failed: {e}") from e


# ========== 提示词加载（从 Markdown） ==========
def _is_engine_overloaded_error(exc: Exception) -> bool:
    text = str(exc).lower()
    is_rate_limit = exc.__class__.__name__ == "RateLimitError" or "429" in text
    overloaded = "engine_overloaded_error" in text or "currently overloaded" in text or "overloaded" in text
    return is_rate_limit and overloaded


def _call_with_overload_retry(func, operation_name: str):
    """
    针对 OpenAI 429 engine_overloaded 错误重试：总尝试 3 次，间隔 5s、10s。
    """
    retry_delays = [5, 10]
    for attempt in range(1, 4):
        try:
            return func()
        except Exception as e:
            if attempt < 3 and _is_engine_overloaded_error(e):
                wait_seconds = retry_delays[attempt - 1]
                print(f"[retry] {operation_name} 发生过载，{wait_seconds}s 后重试（第 {attempt + 1}/3 次）")
                time.sleep(wait_seconds)
                continue
            raise


PROMPTS_PATH = PRASE_SKILL_DIR / "resources" / "prompts" / "prompts.md"
_PROMPTS_CACHE: Dict[str, str] | None = None


def _load_prompts_from_md(md_path: Path) -> Dict[str, str]:
    """
    解析 prompts.md，按 '### name' 分段，返回 {name: content}。
    """
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    prompts: Dict[str, str] = {}
    current_name: str | None = None
    buffer: list[str] = []
    for line in lines:
        if line.startswith("### "):
            if current_name is not None:
                prompts[current_name] = ("\n".join(buffer)).strip()
                buffer = []
            current_name = line[len("### "):].strip()
        else:
            buffer.append(line)
    if current_name is not None:
        prompts[current_name] = ("\n".join(buffer)).strip()
    return prompts


def get_prompt(prompt_name: str) -> str:
    """
    从 prompts.md 获取提示词；若不存在，返回空字符串
    """
    global _PROMPTS_CACHE
    if _PROMPTS_CACHE is None:
        if not PROMPTS_PATH.exists():
            return ""
        _PROMPTS_CACHE = _load_prompts_from_md(PROMPTS_PATH)
    return _PROMPTS_CACHE.get(prompt_name, "")


def extract_content_from_url(document_url, prompt, api_key=None, max_tokens=128000):
    """
    从文档 URL 或本地文件提取内容，并让模型基于文档内容完成提示词任务。
    """
    load_env_config()
    if api_key is None:
        api_key = os.environ.get("LLM_API_KEY")
    try:
        from openai import OpenAI  # type: ignore
    except ImportError:
        raise ImportError("OpenAI library is required. Please install it with: pip install openai")

    client = OpenAI(
        api_key=api_key,
        base_url=os.environ.get("LLM_BASE_URL")
    )

    try:
        # 判断是本地路径还是 http/https
        parsed = urllib.parse.urlparse(str(document_url))
        is_http = parsed.scheme in ("http", "https")
        if not is_http:
            # 当作本地文件处理
            print(f"检测到本地文件: {document_url}")
            if not os.path.exists(document_url):
                raise FileNotFoundError(f"文件不存在: {document_url}")
            def _create_local():
                with open(document_url, "rb") as f:
                    return client.files.create(file=f, purpose="file-extract")
            file_object = _call_with_overload_retry(
                _create_local,
                operation_name="files.create(local)"
            )
        else:
            # 远程URL：先下载到内存再上传
            print(f"检测到URL: {document_url}")
            def _download_and_upload():
                with urllib.request.urlopen(document_url, timeout=30) as resp:
                    data = resp.read()
                bio = BytesIO(data)
                bio.name = Path(parsed.path).name or "document"
                return client.files.create(file=bio, purpose="file-extract")
            file_object = _call_with_overload_retry(
                _download_and_upload,
                operation_name="files.create(url)"
            )

        file_id = file_object.id
        print(f"文件上传成功，ID: {file_id}")

        file_content = _call_with_overload_retry(
            lambda: client.files.content(file_id=file_id).text,
            operation_name="files.content"
        )
        print("文件内容提取完成")

        messages = [
            {
                "role": "system",
                "content": "你是LLM，人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视、黄色暴力等问题的回答。"
            },
            {
                "role": "system",
                "content": file_content
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        completion = _call_with_overload_retry(
            lambda: client.chat.completions.create(
                model=os.environ.get("LLM_MODEL"),
                messages=messages,
                temperature=0.6,
                max_tokens=max_tokens
            ),
            operation_name="chat.completions.create(with_file_content)"
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"请求失败: {e}")
        import traceback
        traceback.print_exc()
        return f"处理失败: {e}"


def parse_industry_result(raw: str) -> dict:
    text = raw.strip()
    if text.startswith("{"):
        try:
            data = json.loads(text) if "}" in text else {}
            if isinstance(data, dict):
                l1 = data.get("industry_level1", data.get("level1", ""))
                l2 = data.get("industry_level2", data.get("level2", ""))
                if l1 or l2:
                    label = f"{l1}/{l2}" if l2 else str(l1)
                    return {"industry_level1": str(l1), "industry_level2": str(l2), "industry_label": label}
        except Exception:
            pass
    if "/" in text:
        parts = [p.strip() for p in text.split("/", 1)]
        level1 = parts[0] if parts else ""
        level2 = parts[1] if len(parts) > 1 else ""
    else:
        level1 = text
        level2 = ""
    label = f"{level1}/{level2}" if level2 else level1
    return {"industry_level1": level1, "industry_level2": level2, "industry_label": label}


def step1_industry_identification(
    bid_doc_path: str | None = None,
    industry_class_file_path: str | None = None,
):
    print("\n" + "="*60)
    print("步骤1: 行业识别")
    print("="*60)
    bid_doc = Path(bid_doc_path) if bid_doc_path else (PRASE_SKILL_DIR / "招标文件.pdf")
    industry_class_file = (
        Path(industry_class_file_path)
        if industry_class_file_path
        else (PRASE_SKILL_DIR / "industry_class.md")
    )
    industry_class = ""
    if industry_class_file.exists():
        with open(industry_class_file, "r", encoding="utf-8") as f:
            industry_class = f.read()
    prompt = get_prompt("industry_class")
    prompt = prompt.format(industry_class=industry_class)
    print(f"招标文件: {bid_doc}")
    print("正在调用LLM模型进行行业识别...")
    result = extract_content_from_url(str(bid_doc), prompt)
    print(f"行业识别结果: {result}")
    data = parse_industry_result(str(result))
    return data


def _normalize_content_structured(data: dict) -> dict:
    if not isinstance(data, dict):
        return {"template_type": "extraction", "modules": []}
    modules_raw = data.get("modules", [])
    if not modules_raw:
        return {"template_type": data.get("template_type", "extraction"), "modules": []}

    def _sanitize_item(it):
        if not isinstance(it, dict):
            return None
        return {
            "item_name": it.get("item_name", ""),
            "description": it.get("description", ""),
        }

    by_m1: Dict[str, list] = {}
    for m in modules_raw:
        if not isinstance(m, dict):
            continue
        m1 = m.get("module_level1", "")
        children_raw = m.get("children")
        m2 = m.get("module_level2", "")
        items_raw = m.get("items", [])

        if children_raw is not None:
            children = []
            for ch in children_raw if isinstance(children_raw, list) else []:
                if not isinstance(ch, dict):
                    continue
                items = [_sanitize_item(it) for it in (ch.get("items") or []) if isinstance(it, dict)]
                items = [x for x in items if x and x.get("item_name")]
                children.append({
                    "module_level2": ch.get("module_level2", ""),
                    "items": items,
                })
            if m1 not in by_m1:
                by_m1[m1] = []
            by_m1[m1].extend(children)
        else:
            items = [_sanitize_item(it) for it in (items_raw if isinstance(items_raw, list) else []) if isinstance(it, dict)]
            items = [x for x in items if x and x.get("item_name")]
            child = {"module_level2": m2 if m2 is not None else "", "items": items}
            if m1 not in by_m1:
                by_m1[m1] = []
            by_m1[m1].append(child)

    result_modules = [
        {"module_level1": m1, "children": ch_list}
        for m1, ch_list in by_m1.items()
    ]
    return {"template_type": data.get("template_type", "extraction"), "modules": result_modules}


def step2_load_industry_template(
    industry_data: dict,
    template_dir_path: str | None = None,
    base_template_name: str = "通用行业"
) -> dict:
    print("\n" + "=" * 60)
    print("步骤2: 加载行业模板")
    print("=" * 60)
    level1 = industry_data.get("industry_level1", "")
    level2 = industry_data.get("industry_level2", "")
    label = industry_data.get("industry_label", f"{level1}/{level2}" if level2 else level1)
    print(f"行业: {label}")
    template_dir = Path(template_dir_path) if template_dir_path else (PRASE_SKILL_DIR / "resources" / "source_industry_key")
    base_file = template_dir / f"{base_template_name}.md"
    if base_file.exists():
        with open(base_file, "r", encoding="utf-8") as f:
            base_content = f.read().rstrip()
        print(f"基础模板已加载: {base_file}，长度 {len(base_content)} 字符")
    else:
        base_content = ""
        print(f"未找到基础模板: {base_file}，跳过")
    if level1 and level2:
        industry_file = template_dir / level1 / f"{level2}.md"
    else:
        industry_file = template_dir / "通用行业.md"
    if industry_file.exists():
        with open(industry_file, "r", encoding="utf-8") as f:
            industry_content = f.read().rstrip()
        print(f"行业模板已加载: {industry_file}，长度 {len(industry_content)} 字符")
    else:
        print(f"未找到行业模板: {industry_file}，使用通用行业模板")
        industry_file = template_dir / "通用行业.md"
        with open(industry_file, "r", encoding="utf-8") as f:
            industry_content = f.read().rstrip()
    if base_file.resolve() == industry_file.resolve():
        content = base_content or industry_content
    else:
        content = "\n\n---\n\n".join(filter(None, [base_content, industry_content]))
    print(f"合并后模板总长度: {len(content)} 字符")
    print("正在调用LLM模型生成JSON结构化抽取模板...")
    client = LLMClient()
    prompt = get_prompt("structure_extraction_template")
    prompt = prompt.replace("{merged_template}", content)
    raw_json = client.chat(user_prompt=prompt)
    try:
        content_structured = safe_json_loads(raw_json)
    except Exception as e:
        print(f"警告: 结构化解析失败 ({e})，content_structured 为空对象")
        content_structured = {"template_type": "extraction", "modules": []}
    content_structured = _normalize_content_structured(content_structured)
    print("JSON 结构化抽取模板已生成")
    result = {
        "base_template_path": str(base_file),
        "industry_template_path": str(industry_file),
        "content_structured": content_structured,
    }
    return result


def _load_industry_template_md(tmpl: dict) -> str:
    md = tmpl.get("content", "")
    if md:
        return md
    base_path = tmpl.get("base_template_path")
    industry_path = tmpl.get("industry_template_path")
    if base_path and industry_path:
        base_p = Path(base_path)
        industry_p = Path(industry_path)
        if not base_p.exists():
            base_p = PRASE_SKILL_DIR / base_path
        if not industry_p.exists():
            industry_p = PRASE_SKILL_DIR / industry_path
        base_content = base_p.read_text(encoding="utf-8").rstrip() if base_p.exists() else ""
        industry_content = industry_p.read_text(encoding="utf-8").rstrip() if industry_p.exists() else ""
        if base_p.resolve() == industry_p.resolve():
            return base_content or industry_content
        return "\n\n---\n\n".join(filter(None, [base_content, industry_content]))
    return ""


def step3_requirement_extraction(
    industry_name: str,
    industry_template: str,
    template_structure: dict | None = None,
    bid_doc_path: str | None = None
) -> dict:
    print("\n" + "=" * 60)
    print("步骤3: 招标要求抽取")
    print("=" * 60)
    bid_doc = Path(bid_doc_path) if bid_doc_path else (PRASE_SKILL_DIR / "招标文件.pdf")
    prompt = get_prompt("extractor")
    prompt = prompt.format(
        industry_name=industry_name,
        industry_extract_template=industry_template
    )
    print(f"招标文件: {bid_doc}")
    print(f"行业名称: {industry_name}")
    print("正在调用LLM模型抽取招标要求...")
    raw_response = extract_content_from_url(str(bid_doc), prompt)
    print(f"模型响应长度: {len(raw_response)} 字符")
    content_structured = None
    try:
        content_structured = safe_json_loads(raw_response)
        if content_structured and isinstance(content_structured, dict):
            print("JSON解析成功")
        else:
            print("警告: JSON解析结果为空或格式不正确")
            content_structured = {"template_type": "extraction_result", "modules": []}
    except Exception as e:
        print(f"警告: JSON解析失败 ({e})，尝试从Markdown提取...")
        if template_structure:
            content_structured = _parse_markdown_to_structure(raw_response, template_structure)
    result = {
        "document_title": "招标要求抽取结果",
        "content_structured": content_structured,
        "extracted_at": datetime.now().isoformat(),
    }
    return result


def _parse_markdown_to_structure(content_md: str, template_structure: dict) -> dict:
    result_modules = []
    modules = template_structure.get('modules', [])
    for module in modules:
        module_level1 = module.get('module_level1', '')
        children = module.get('children', [])
        result_children = []
        for child in children:
            module_level2 = child.get('module_level2', '')
            items = child.get('items', [])
            result_items = []
            for item in items:
                item_name = item.get('item_name', '')
                content = _extract_item_content(content_md, module_level1, module_level2, item_name)
                result_items.append({
                    "item_name": item_name,
                    "content": content if content else ""
                })
            result_children.append({
                "module_level2": module_level2,
                "items": result_items
            })
        result_modules.append({
            "module_level1": module_level1,
            "children": result_children
        })
    return {
        "template_type": "extraction_result",
        "modules": result_modules
    }


def _extract_item_content(content_md: str, module_level1: str, module_level2: str, item_name: str) -> str:
    lines = content_md.split('\n')
    result: list[str] = []
    capturing = False
    capture_level = 0
    m1_clean = module_level1.replace('、', ' ').replace('#', '').strip()
    m2_clean = module_level2.replace('、', ' ').replace('#', '').strip() if module_level2 else ""
    item_clean = item_name.strip()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith('# ') or stripped.startswith('## '):
            title = stripped.replace('# ', '').replace('## ', '').strip()
            if m1_clean in title or title in m1_clean:
                capturing = True
                capture_level = 1
                i += 1
                continue
            elif capturing and capture_level == 1:
                break
        if capturing and m2_clean:
            if stripped.startswith('## ') or stripped.startswith('### ') or stripped.startswith('#### '):
                title = stripped.replace('## ', '').replace('### ', '').replace('#### ', '').strip()
                if m2_clean in title or title in m2_clean:
                    capture_level = 2
                    i += 1
                    continue
                elif capture_level == 2 and (stripped.startswith('## ') or stripped.startswith('### ')):
                    break
        if capturing and (not m2_clean or capture_level >= 2):
            is_target = False
            if item_clean in stripped:
                is_target = True
            if not is_target and ('评分' in item_clean and '评分' in stripped):
                is_target = True
            if not is_target and ('条款' in item_clean and '条款' in stripped):
                is_target = True
            if not is_target and ('资质' in item_clean and '资质' in stripped):
                is_target = True
            if not is_target and ('人员' in item_clean and '人员' in stripped):
                is_target = True
            if is_target:
                i += 1
                while i < len(lines):
                    content_line = lines[i]
                    content_stripped = content_line.strip()
                    if content_stripped.startswith('# '):
                        break
                    if content_stripped.startswith('## ') and m2_clean:
                        break
                    if content_stripped:
                        result.append(content_line)
                    elif result and not content_stripped:
                        if result[-1].strip():
                            result.append(content_line)
                    i += 1
                return '\n'.join(result).strip()
        i += 1
    return '\n'.join(result).strip()

@contextmanager
def suppress_output():
    """
    静默上下文：屏蔽 stdout/stderr，确保“一键执行”仅输出最终结果信息
    """
    f_out, f_err = StringIO(), StringIO()
    with redirect_stdout(f_out), redirect_stderr(f_err):
        yield


def print_qr_to_terminal(content: str) -> None:
    """
    在终端打印ASCII二维码；若缺少依赖则给出提示。
    """
    try:
        import qrcode  # type: ignore
        qr = qrcode.QRCode(border=1)
        qr.add_data(content)
        qr.make(fit=True)
        print("\n二维码（微信终端扫码）：")
        qr.print_ascii(invert=True)
    except ImportError:
        print("\n未安装 qrcode 库，无法在终端打印二维码。可安装后重试：pip install qrcode")
    except Exception as e:
        print(f"\n终端二维码打印失败：{e}")


def select_bid_doc_via_dialog() -> str | None:
    """
    通过系统文件选择弹窗选择招标PDF文件。
    返回文件路径；若取消或不可用则返回 None。
    """
    try:
        import tkinter as tk  # type: ignore
        from tkinter import filedialog  # type: ignore
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        file_path = filedialog.askopenfilename(
            title="请选择招标文件（PDF）",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
        )
        root.destroy()
        return file_path or None
    except Exception as e:
        print(f"文件选择弹窗不可用：{e}")
        return None


def _is_http_url(text: str) -> bool:
    try:
        p = urllib.parse.urlparse(str(text))
        return p.scheme in ("http", "https") and bool(p.netloc)
    except Exception:
        return False


def prompt_bid_doc_in_terminal(max_retries: int = 3) -> str | None:
    """
    终端兜底交互：提示用户输入本地PDF路径或http/https链接。
    校验存在性或URL合法性，失败重试，超过次数返回 None。
    """
    for i in range(max_retries):
        try:
            user_in = input("请输入招标文件路径（本地PDF路径或http/https链接），回车确认：").strip().strip('"').strip("'")
        except EOFError:
            user_in = ""
        if not user_in:
            print("未输入内容。")
            continue
        if _is_http_url(user_in):
            print(f"检测到URL：{user_in}")
            return user_in
        if os.path.exists(user_in) and os.path.isfile(user_in):
            print(f"检测到本地文件：{user_in}")
            return user_in
        print("路径无效或文件不存在，请重试。")
    return None


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _get_local_ip() -> str:
    """
    获取本机局域网 IP，失败则退回 127.0.0.1
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def _get_free_port() -> int:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def start_static_http_server_for(directory: Path) -> tuple[subprocess.Popen, str]:
    """
    在后台启动一个独立静态文件 HTTP 服务进程，服务根目录为 directory。
    返回 (process, base_url)
    """
    port = _get_free_port()
    cmd = [sys.executable, "-m", "http.server", str(port), "--bind", "0.0.0.0"]
    kwargs: Dict[str, Any] = {
        "cwd": str(directory),
        "stdout": subprocess.DEVNULL,
        "stderr": subprocess.DEVNULL,
    }
    if os.name == "nt":
        kwargs["creationflags"] = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        kwargs["start_new_session"] = True
    proc = subprocess.Popen(cmd, **kwargs)
    ip = _get_local_ip()
    base_url = f"http://{ip}:{port}"
    return proc, base_url


def final_json_to_rows(final_data: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    将最终的 content_structured 转为按行的数据：
    列：module_level1, module_level2, item_name, content
    """
    rows: List[Dict[str, str]] = []
    content_structured = (final_data or {}).get("content_structured") or {}
    for m in content_structured.get("modules", []):
        m1 = str(m.get("module_level1", "") or "")
        for ch in m.get("children", []) or []:
            m2 = str(ch.get("module_level2", "") or "")
            for it in ch.get("items", []) or []:
                rows.append({
                    "module_level1": m1,
                    "module_level2": m2,
                    "item_name": str(it.get("item_name", "") or ""),
                    "content": str(it.get("content", "") or ""),
                })
    return rows

def write_pdf(
    rows: List[Dict[str, str]],
    out_pdf: Path,
    title: str = "招标要求解析结果预览",
    marketing_text: str | None = None,
    wechat_image_path: str | None = None,
) -> None:
    """
    生成PDF文件，包含表格数据和信息
    """
    # 初始化中文字体变量
    chinese_font_name = "ChineseFont"
    
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.pdfbase.cidfonts import UnicodeCIDFont
        from reportlab.lib.enums import TA_LEFT, TA_CENTER
        import platform
        
        # 注册中文字体
        chinese_font_registered = False
        
        # 尝试注册系统中文字体
        system_fonts = []
        if platform.system() == "Windows":
            # Windows系统字体路径
            system_fonts = [
                ("C:/Windows/Fonts/simsun.ttc", "SimSun"),  # 宋体
                ("C:/Windows/Fonts/simhei.ttf", "SimHei"),  # 黑体
                ("C:/Windows/Fonts/msyh.ttc", "MicrosoftYaHei"),  # 微软雅黑
                ("C:/Windows/Fonts/simkai.ttf", "KaiTi"),  # 楷体
            ]
        elif platform.system() == "Darwin":  # macOS
            system_fonts = [
                ("/System/Library/Fonts/PingFang.ttc", "PingFang"),
                ("/System/Library/Fonts/STHeiti Light.ttc", "STHeiti"),
            ]
        else:  # Linux
            system_fonts = [
                ("/usr/share/fonts/truetype/wqy/wqy-microhei.ttc", "WenQuanYi"),
                ("/usr/share/fonts/truetype/arphic/uming.ttc", "AR PL UMing"),
            ]
        
        # 尝试注册第一个可用的中文字体
        for font_path, font_alias in system_fonts:
            try:
                if os.path.exists(font_path):
                    pdfmetrics.registerFont(TTFont(chinese_font_name, font_path))
                    chinese_font_registered = True
                    break
            except Exception:
                continue
        
        # 如果系统字体都不可用，尝试使用reportlab内置的CJK字体
        if not chinese_font_registered:
            try:
                pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))  # 使用内置宋体
                chinese_font_name = "STSong-Light"
                chinese_font_registered = True
            except Exception:
                pass
        
        # 如果仍然无法注册中文字体，抛出异常提示使用weasyprint
        if not chinese_font_registered:
            raise ImportError("无法注册中文字体，将尝试使用weasyprint")
            
    except ImportError:
        # 如果reportlab不可用，尝试使用weasyprint
        try:
            from weasyprint import HTML, CSS
            import html as html_escape
            import tempfile
            
            ensure_parent(out_pdf)
            # 生成临时HTML
            thead = "<tr><th>一级模块</th><th>二级模块</th><th>抽取项</th><th>内容</th></tr>"
            trs = []
            for r in rows:
                tds = "".join([
                    f"<td>{html_escape.escape(r.get('module_level1',''))}</td>",
                    f"<td>{html_escape.escape(r.get('module_level2',''))}</td>",
                    f"<td>{html_escape.escape(r.get('item_name',''))}</td>",
                    f"<td style='white-space:pre-wrap'>{html_escape.escape(r.get('content',''))}</td>",
                ])
                trs.append(f"<tr>{tds}</tr>")
            
            table_html = f"<table border='1' cellpadding='5' cellspacing='0' style='width:100%;border-collapse:collapse;'><thead>{thead}</thead><tbody>{''.join(trs)}</tbody></table>"
            summary_html = f"<p>共 <strong>{len(rows)}</strong> 条抽取结果，更详细解析请前往标书魔方官网：https://biaoshu.supcon.com/，让 AI 成为你的投标得力助手！</p>"
            
            html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body {{ font-family: "Microsoft YaHei", Arial, sans-serif; padding: 20px; }}
h1 {{ font-size: 20px; }}
table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
th {{ background-color: #f2f2f2; font-weight: bold; }}
</style>
</head>
<body>
<h1>{html_escape.escape(title)}</h1>
{summary_html}
{table_html}
</body>
</html>"""
            
            HTML(string=html_content).write_pdf(out_pdf)
            return
        except ImportError:
            raise ImportError("需要安装 reportlab 或 weasyprint 库来生成PDF。请运行: pip install reportlab 或 pip install weasyprint")
    
    ensure_parent(out_pdf)
    
    # 创建PDF文档
    doc = SimpleDocTemplate(
        str(out_pdf),
        pagesize=landscape(A4),
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # 准备内容列表
    story = []
    styles = getSampleStyleSheet()
    
    # 标题样式（使用中文字体）
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName=chinese_font_name
    )
    
    # 正文样式（使用中文字体）
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#1f2937'),
        leading=14,
        alignment=TA_LEFT,
        fontName=chinese_font_name
    )
    
    # 表格单元格样式（支持换行）
    table_cell_style = ParagraphStyle(
        'TableCellStyle',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#1f2937'),
        leading=12,
        alignment=TA_LEFT,
        fontName=chinese_font_name,
        wordWrap='CJK'  # 支持中文换行
    )
    
    # 表格表头样式
    table_header_style = ParagraphStyle(
        'TableHeaderStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#0f172a'),
        leading=14,
        alignment=TA_LEFT,
        fontName=chinese_font_name,
        wordWrap='CJK'
    )
    
    # 添加标题
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 0.5*cm))
    
    # 添加摘要
    summary_text = f"共 <b>{len(rows)}</b> 条抽取结果，更详细解析请前往标书魔方官网：https://biaoshu.supcon.com/，让 AI 成为你的投标得力助手！"
    story.append(Paragraph(summary_text, normal_style))
    story.append(Spacer(1, 0.5*cm))
    
    # 定义转义函数（用于表格和文本）
    def escape_text(text):
        """转义HTML特殊字符"""
        if not text:
            return ""
        text = str(text)
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('\n', '<br/>')
        return text
    
    if not rows:
        story.append(Paragraph("未抽取到结果，请检查输入文件或模板配置。", normal_style))
    else:
        # 准备表格数据（使用Paragraph包装以支持换行）
        
        table_data = [[
            Paragraph(escape_text('一级模块'), table_header_style),
            Paragraph(escape_text('二级模块'), table_header_style),
            Paragraph(escape_text('抽取项'), table_header_style),
            Paragraph(escape_text('内容'), table_header_style)
        ]]
        for r in rows:
            table_data.append([
                Paragraph(escape_text(r.get('module_level1', '')), table_cell_style),
                Paragraph(escape_text(r.get('module_level2', '')), table_cell_style),
                Paragraph(escape_text(r.get('item_name', '')), table_cell_style),
                Paragraph(escape_text(r.get('content', '')), table_cell_style)
            ])
        
        # 创建表格（使用中文字体，支持换行）
        table = Table(table_data, colWidths=[4*cm, 5*cm, 5.5*cm, 10*cm], repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8fafc')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#0f172a')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#1f2937')),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fcfdff')]),
        ]))
        
        story.append(table)
    
    # 添加信息
    if marketing_text:
        story.append(Spacer(1, 1*cm))
        #story.append(Paragraph("----体验完整功能----", normal_style))
        story.append(Spacer(1, 0.3*cm))
        
        # 处理文本
        marketing_lines = marketing_text.split('\n')
        for line in marketing_lines:
            if line.strip():
                story.append(Paragraph(escape_text(line.strip()), normal_style))
                story.append(Spacer(1, 0.2*cm))
        
        # 添加微信二维码图片（支持本地路径或http/https链接）
        if wechat_image_path:
            try:
                if str(wechat_image_path).startswith(("http://", "https://")):
                    with urllib.request.urlopen(wechat_image_path, timeout=10) as resp:
                        img_bytes = resp.read()
                    img = Image(BytesIO(img_bytes), width=6*cm, height=6*cm)
                elif Path(wechat_image_path).exists():
                    img = Image(wechat_image_path, width=6*cm, height=6*cm)
                else:
                    img = None
                if img is not None:
                    story.append(Spacer(1, 0.3*cm))
                    story.append(img)
            except Exception:
                pass
    
    # 构建PDF
    doc.build(story)


def run_pipeline(
    bid_doc: str,
    out_pdf: str,
    industry_class_file: str | None = None,
    template_dir: str | None = None,
    max_integrity_retries: int = 2,
    max_compliance_retries: int = 2,
) -> Path:
    """
    一键静默执行全流程，仅在结束后输出最终 pdf 文件。
    """
    def _print_json(data: Any) -> None:
        """
        统一的步骤结果打印：带步骤号 + 彩色边框 + 美化 JSON。
        """
        # 美化 JSON 输出，避免一行过长
        try:
            text = json.dumps(data, ensure_ascii=False, indent=2)
        except Exception:
            text = str(data)
        print(text)

    # 步骤 1：行业识别
    print("第一步抽取行业开始\n")
    with suppress_output():
        ind = step1_industry_identification(
            bid_doc_path=bid_doc,
            industry_class_file_path=industry_class_file
        )
    print(json.dumps(ind, ensure_ascii=False, indent=2))
    print("第一步抽取行业完成\n\n")

    # 步骤 2：加载行业模板
    print("第二步获取行业模板开始\n")
    with suppress_output():
        tmpl = step2_load_industry_template(
            ind,
            template_dir_path=template_dir,
            base_template_name="通用行业"
        )
    print("第二步获取行业模板完成\n\n")

    # 准备模板 Markdown/结构
    print("第三步生成解析项开始\n")
    industry_template_md = _load_industry_template_md(tmpl)
    template_structure = tmpl.get("content_structured", None)
    industry_name = ind.get("industry_label", "")
    # 步骤 3：抽取
    with suppress_output():
        req_data = step3_requirement_extraction(
            industry_name=industry_name,
            industry_template=industry_template_md,
            template_structure=template_structure,
            bid_doc_path=bid_doc
        )
    print("第三步生成解析项完成\n\n")

    # 最终结果直接来自内存
    final_json = req_data
    rows = final_json_to_rows(final_json)
    print("开始生成PDF\n")
    # 输出 PDF
    out_pdf_path = Path(out_pdf)
    marketing_text = (
        "----体验完整功能----\n"
        "【标书魔方】从正文智能生成、专业图文排版到合规格式校验，全流程自动化赋能，让你告别繁琐排版、重复码字，大幅提升投标文件撰写效率与专业度。\n"
        "如需体验完整功能，立即前往官网：https://biaoshu.supcon.com/?scene=01010040\n"
        "让 AI 成为你的投标得力助手！\n"
        "-----社群福利-----\n"
        "加入「标书魔方」官方社群，你能解锁：\n"
        "√ 免费领取行业标卡模板与精品资料包\n"
        "√ 参与抽奖赢取实用办公好物与会员权益\n"
        "√ 第一时间获取产品更新动态与投标技巧\n"
        "扫码进群，和万千同行一起高效写标、轻松中标！"
    )
    wechat_img = WECHAT_IMAGE_URL
    write_pdf(rows, out_pdf_path, marketing_text=marketing_text, wechat_image_path=wechat_img)
    print("生成PDF完成\n\n")
    print("PDF文件地址：" + str(out_pdf_path.resolve()) + "\n\n")
    return out_pdf_path


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="一键运行全流程并输出最终 PDF 文件")
    parser.add_argument("--bid-doc", dest="bid_doc", required=False, help="招标文件路径（PDF）")
    args = parser.parse_args()
    bid_doc = args.bid_doc
    if not bid_doc:
        print("未传入 --bid-doc，正在打开文件选择窗口...")
        bid_doc = select_bid_doc_via_dialog()
        if not bid_doc:
            print("文件选择弹窗不可用或已取消，切换为命令行输入模式。")
            bid_doc = prompt_bid_doc_in_terminal()
            if not bid_doc:
                raise SystemExit("未提供有效的招标文件路径或URL，程序结束。")
    print(f"本次使用招标文件：{bid_doc}")

    # 固定PDF输出地址（无需命令行配置）
    fixed_preview_pdf = PRASE_SKILL_DIR / "final_result_preview.pdf"
    preview_pdf_path = run_pipeline(
        bid_doc=bid_doc,
        out_pdf=str(fixed_preview_pdf)
    )

    # 输出PDF文件路径
    result: Dict[str, Any] = {
        "preview_pdf": str(preview_pdf_path),
        "preview_pdf_path": str(preview_pdf_path.resolve()),
    }
    print(json.dumps(result, ensure_ascii=False))
    print("\nPDF文件地址：")
    print(result["preview_pdf_path"])
    # 启动本地 HTTP 服务并打印可预览地址
    try:
        proc, base_url = start_static_http_server_for(preview_pdf_path.parent)
        pdf_url = f"{base_url}/{urllib.parse.quote(preview_pdf_path.name)}"
        print("本地HTTP预览地址：")
        print(pdf_url)
        print(f"HTTP预览服务后台已启动（PID: {proc.pid}）")
    except Exception as e:
        print(f"本地HTTP预览地址生成失败：{e}")
    print(
        "\n----体验完整功能----\n"
        "【标书魔方】从正文智能生成、专业图文排版到合规格式校验，全流程自动化赋能，让你告别繁琐排版、重复码字，大幅提升投标文件撰写效率与专业度。\n"
        "如需体验完整功能，立即前往官网：https://biaoshu.supcon.com/?scene=01010040\n"
        "让 AI 成为你的投标得力助手！\n"
        "-----社群福利-----\n"
        "加入「标书魔方」官方社群，你能解锁：\n"
        "√ 免费领取行业标卡模板与精品资料包\n"
        "√ 参与抽奖赢取实用办公好物与会员权益\n"
        "√ 第一时间获取产品更新动态与投标技巧\n"
        "扫码进群，和万千同行一起高效写标、轻松中标！https://aistatic.supcon.com/tender/assets/jpg/home_link-Dwolmpjc.jpg"
    )
    print_qr_to_terminal(WECHAT_IMAGE_URL)

