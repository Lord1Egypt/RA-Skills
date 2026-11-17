#!/usr/bin/env python3
"""BIMWing (垒知翼) API 直连客户端：登录 -> 上传 -> 等待转码 -> 生成分享链接。

主路径：直接调用 BIMWing 后端接口（无头、快）。
兜底路径见 bimwing_browser.py（Playwright 驱动网页）。

凭证：环境变量 BIMWING_MOBILE / BIMWING_PASSWORD，或同目录 config.local.json（本地私有，gitignore），
      或同目录 config.json（分享模板，默认空）。无任何凭证时由 agent 向用户索取并写入 config.local.json。

已确认协议（来自前端逆向 + 实测）：
  - 登录: POST /app-api/system/member/auth/login
          body={mobile, password, versionStatus:true} -> Bearer token
  - 上传: POST /app-api/business/model-file/modelUpload (multipart/form-data)
  - 转码进度: GET /app-api/business/model-file/getProgress?id=<id> -> 数字 0~100（100=完成）
  - 模型详情: GET /app-api/business/model-file/modelDetail?id=<id>
             coverStatus: 2=可看, 3=转换失败
  - 分享: GET /app-api/business/model-file-share/get?cipherFileId=<cipher>&add=1
          -> 服务端生成分享记录（data.fileId）
  - 分享链接: https://bimwing.letsgrp.com/share-view?shareId=<cipher>&type=<modelType>
    其中 cipher = AES-128-ECB(PKCS7, base64), key="isjdhwngjskdiwjt", 明文=模型数字 id
"""
import os
import sys
import time
import json
import base64
import datetime

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

API_BASE = "https://bimwing-api.letsgrp.com"
WEB_BASE = "https://bimwing.letsgrp.com"
REGISTER_URL = "https://bimwing.letsgrp.com/sign-in"  # 「免费注册」按钮跳转地址，无账号先在此注册
CIPHER_KEY = b"isjdhwngjskdiwjt"  # 16字节，AES-128


def register_hint():
    """打印注册提示（无账号时给用户看）。"""
    print(f"还没有 BIMWing 账号？请先在此注册：{REGISTER_URL}")


def load_credentials():
    mobile = os.environ.get("BIMWING_MOBILE")
    password = os.environ.get("BIMWING_PASSWORD")
    if mobile and password:
        return mobile, password
    # 优先读本机私有配置（gitignore，含真实凭证）；其次读分享用的模板 config.json
    base = os.path.dirname(os.path.abspath(__file__))
    for name in ("config.local.json", "config.json"):
        cfg = os.path.join(base, name)
        if os.path.exists(cfg):
            try:
                with open(cfg, "r", encoding="utf-8") as f:
                    d = json.load(f)
            except Exception:
                continue
            m, p = d.get("mobile"), d.get("password")
            if m and p:
                return m, p
    return None, None


def save_credentials(mobile, password, private=True):
    """把凭证写回本地配置文件。private=True 写 config.local.json（gitignore，不随 skill 分享）。

    注意：BIMWing 仅支持手机号+密码登录，凭证以明文存储。写入后收窄文件权限为 600
    （仅当前用户可读写），降低被本机其他用户/进程读取的风险。调用方必须在获得用户
    明确同意后才可调用本函数。
    """
    base = os.path.dirname(os.path.abspath(__file__))
    name = "config.local.json" if private else "config.json"
    path = os.path.join(base, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"mobile": mobile, "password": password}, f, ensure_ascii=False, indent=2)
    # 收窄文件权限，降低明文凭证被本机其他用户/进程读取的风险
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass


def cipher_id(model_id) -> str:
    """与前端 KMe 一致的加密：AES-128-ECB / PKCS7 / base64。"""
    pt = str(model_id).encode("utf-8")
    ct = AES.new(CIPHER_KEY, AES.MODE_ECB).encrypt(pad(pt, 16))
    return base64.b64encode(ct).decode("ascii")


class BimwingClient:
    def __init__(self, mobile, password, timeout=120):
        self.mobile = mobile
        self.password = password
        self.timeout = timeout
        self.session = requests.Session()
        self.token = None
        self.refresh_token = None
        self.user_id = None

    # ---------- 鉴权 ----------
    def login(self):
        url = f"{API_BASE}/app-api/system/member/auth/login"
        body = {"mobile": self.mobile, "password": self.password, "versionStatus": True}
        r = self.session.post(url, json=body, timeout=self.timeout)
        r.raise_for_status()
        data = r.json()
        if data.get("code") not in (0, 200, None):
            raise RuntimeError(f"登录失败: {data.get('msg')} | {data}")
        d = data.get("data") or {}
        self.token = d.get("accessToken") or d.get("token") or d.get("access_token")
        self.refresh_token = d.get("refreshToken") or d.get("refresh_token")
        self.user_id = d.get("userId") or d.get("user_id") or d.get("id")
        if not self.token:
            raise RuntimeError(f"登录响应缺少 token: {data}")
        self.session.headers.update({"Authorization": f"Bearer {self.token}"})
        return d

    def _auth_refresh(self):
        if not self.refresh_token:
            self.login()
            return
        url = f"{API_BASE}/app-api/system/member/auth/refresh-token"
        r = self.session.post(url, params={"refreshToken": self.refresh_token}, timeout=self.timeout)
        data = r.json()
        if data.get("code") not in (0, 200, None):
            self.login()
            return
        d = data.get("data") or {}
        self.token = d.get("accessToken") or d.get("token") or self.token
        self.refresh_token = d.get("refreshToken") or self.refresh_token
        self.session.headers.update({"Authorization": f"Bearer {self.token}"})

    def _request(self, method, path, _depth=0, **kw):
        url = f"{API_BASE}{path}"
        try:
            r = self.session.request(method, url, timeout=self.timeout, **kw)
            if r.status_code == 401 and _depth == 0:
                self._auth_refresh()
                return self._request(method, path, _depth + 1, **kw)
            r.raise_for_status()
            return r.json()
        except requests.HTTPError:
            if r.status_code == 401 and _depth == 0:
                self._auth_refresh()
                return self._request(method, path, _depth + 1, **kw)
            raise

    # ---------- 上传 ----------
    def upload_model(self, file_path, name=None, rendering_mode=4, outer_type=0):
        """上传模型/图纸并触发转码，返回模型数字 id。

        表单字段（来自前端逆向 model 上传组件）：
          - files: 文件本体（字段名是 files，不是 file）
          - mainFileName: 主文件名
          - renderingMode: 渲染方式（默认 4）
          - outerType: 0=模型
        响应 data 即模型数字 id（整数）。
        """
        url = f"{API_BASE}/app-api/business/model-file/modelUpload"
        fname = name or os.path.basename(file_path)
        with open(file_path, "rb") as fh:
            # requests 的 files 会自动带上 boundary；不要手动设 Content-Type
            files = {"files": (fname, fh, "application/octet-stream")}
            data = {
                "mainFileName": fname,
                "renderingMode": rendering_mode,
                "outerType": outer_type,
            }
            r = self.session.post(url, files=files, data=data, timeout=self.timeout)
        r.raise_for_status()
        resp = r.json()
        if resp.get("code") not in (0, 200, None):
            raise RuntimeError(f"上传失败: {resp.get('msg')} | {resp}")
        d = resp.get("data")
        if isinstance(d, int):
            model_id = d
        elif isinstance(d, dict):
            model_id = d.get("id") or d.get("fileId") or d.get("modelId") or d.get("file_id")
        else:
            model_id = None
        # 兜底：取当前账号最新上传的模型
        if model_id is None:
            model_id = self.get_newest_model()["id"]
        self.model_id = model_id
        return model_id

    # ---------- 模型列表（取最新 / 取类型） ----------
    def get_model_list(self, page_no=1, page_size=20):
        r = self._request("POST", "/app-api/business/model-file/getModelList",
                          json={"pageNo": page_no, "pageSize": page_size})
        d = r.get("data") or {}
        return d.get("list") or [], d.get("total", 0)

    def get_newest_model(self):
        lst = self.get_model_list()[0]
        if not lst:
            raise RuntimeError("未找到已上传的模型")
        return lst[0]

    def get_model_type(self, model_id):
        """从模型列表里取该模型的 modelType（用于分享链接的 type 参数）。"""
        for m in self.get_model_list(1, 50)[0]:
            if str(m.get("id")) == str(model_id):
                return m.get("modelType", 1)
        return 1

    # ---------- 等待转码 ----------
    def wait_conversion(self, model_id, interval=5, timeout=1800):
        """轮询 getProgress（0~100），100=完成；coverStatus==3 视为失败。"""
        deadline = time.time() + timeout
        while time.time() < deadline:
            prog = self._request("GET", f"/app-api/business/model-file/getProgress?id={model_id}")
            pct = prog.get("data")
            pct = pct if isinstance(pct, (int, float)) else 0
            # 检测转换失败
            det = self._request("GET", f"/app-api/business/model-file/modelDetail?id={model_id}")
            cover = (det.get("data") or {}).get("coverStatus")
            if cover == 3:
                raise RuntimeError("模型转换失败（coverStatus=3）")
            print(f"[转码中] id={model_id} progress={pct}%")
            if pct >= 100:
                return True
            time.sleep(interval)
        raise TimeoutError(f"转码超时（>{timeout}s）id={model_id}")

    # ---------- 分享 ----------
    def create_share(self, model_id, model_type=None):
        """确保分享记录存在，并返回分享链接。"""
        cipher = cipher_id(model_id)
        # add=1：若不存在则创建分享记录（返回 data.fileId 即 model_id）
        self._request("GET",
                      f"/app-api/business/model-file-share/get?cipherFileId={cipher}&add=1")
        if model_type is None:
            model_type = self.get_model_type(model_id)
        return f"{WEB_BASE}/share-view?shareId={cipher}&type={model_type}"

    # ---------- 查询 ----------
    def get_progress(self, model_id):
        """返回转码进度 0~100（整数）。"""
        prog = self._request("GET", f"/app-api/business/model-file/getProgress?id={model_id}")
        d = prog.get("data")
        return int(d) if isinstance(d, (int, float)) else 0

    @staticmethod
    def cover_text(cover_status):
        return {0: "排队中", 1: "转换中", 2: "已完成", 3: "转换失败"}.get(
            cover_status, f"未知({cover_status})")

    def model_status(self, model_id):
        """返回单个模型的状态字典：id/fileName/coverStatus(文本)/progress/modelType/createTime。
        模型档案字段取自 getModelList（比 modelDetail 更全），进度取实时 getProgress。
        """
        m = None
        for item in self.get_model_list(1, 50)[0]:
            if str(item.get("id")) == str(model_id):
                m = item
                break
        if m is None:
            det = self._request("GET", f"/app-api/business/model-file/modelDetail?id={model_id}")
            m = det.get("data") or {}
        cs = m.get("coverStatus")
        return {
            "id": m.get("id"),
            "fileName": m.get("fileName"),
            "coverStatus": cs,
            "coverText": self.cover_text(cs),
            "progress": self.get_progress(model_id),
            "modelType": m.get("modelType"),
            "createTime": m.get("createTime"),
        }

    def list_models(self, page_no=1, page_size=20):
        """返回当前账号模型列表（原始 list）。"""
        return self.get_model_list(page_no, page_size)[0]

    # ---------- 生成可点击的「打开页」（不含 iframe） ----------
    def make_open_page(self, share_url, title=None):
        """写出一个本地 HTML 打开页：一个可点击的大按钮，点击即在 WorkBuddy
        内置浏览器预览面板里打开 BIMWing 分享链接（非 iframe 内嵌）。
        返回 HTML 文件路径。agent 应调用 present_files 打开该文件。
        """
        title = title or "BIMWing 模型"
        safe_title = (title or "").replace("<", "&lt;").replace(">", "&gt;")
        out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "preview")
        os.makedirs(out_dir, exist_ok=True)
        # 用链接里的 shareId 做文件名，避免覆盖
        import re as _re
        m = _re.search(r"shareId=([^&]+)", share_url)
        slug = m.group(1) if m else "link"
        path = os.path.join(out_dir, f"bimwing_{slug}.html")
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>{safe_title} - BIMWing</title>
<style>
  body {{ font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
         margin:0; min-height:100vh; display:flex; flex-direction:column;
         align-items:center; justify-content:center; background:#f5f7fa; color:#1f2329; }}
  .card {{ background:#fff; padding:40px 48px; border-radius:16px; box-shadow:0 8px 30px rgba(0,0,0,.08);
          text-align:center; max-width:520px; }}
  h1 {{ font-size:20px; margin:0 0 8px; }}
  .sub {{ color:#8a8f99; font-size:13px; margin-bottom:28px; word-break:break-all; }}
  a.open {{ display:inline-block; text-decoration:none; background:#2f6bff; color:#fff;
           font-size:16px; font-weight:600; padding:14px 36px; border-radius:10px;
           transition:.15s; }}
  a.open:hover {{ background:#1f5af0; }}
  .tip {{ margin-top:22px; font-size:12px; color:#a8adb5; }}
</style>
</head>
<body>
  <div class="card">
    <h1>{safe_title}</h1>
    <div class="sub">{share_url}</div>
    <a class="open" href="{share_url}" target="_top">在 WorkBuddy 中打开模型</a>
    <div class="tip">点击上方按钮，即可在内置浏览器预览面板查看模型（无需登录）</div>
  </div>
</body>
</html>
"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        return path

    def format_models(self, page_no=1, page_size=20):
        """返回人类可读的当前账号模型列表（含转码状态），并附带分页信息/翻页提示。"""
        items, total = self.get_model_list(page_no, page_size)
        if not items:
            return "(当前账号暂无模型)"
        total_pages = max(1, (total + page_size - 1) // page_size)
        lines = []
        for m in items:
            mid = m.get("id")
            name = m.get("fileName", "?")
            cs = m.get("coverStatus")
            pct = (self.get_progress(mid) if cs in (0, 1)
                   else (100 if cs == 2 else 0))
            tstr = ""
            ct = m.get("createTime")
            if ct:
                tstr = datetime.datetime.fromtimestamp(ct / 1000).strftime("%Y-%m-%d %H:%M")
            lines.append(f"[{mid}] {name}  | 状态:{self.cover_text(cs)}({pct}%) | 类型:{m.get('modelType')} | 上传:{tstr}")
        footer = f"\n—— 第 {page_no}/{total_pages} 页，共 {total} 个模型 ——"
        if page_no < total_pages:
            next_no = page_no + 1
            footer += f"\n还有更多模型，可说「第 {next_no} 页」或「下一页」继续查看。"
        return "\n".join(lines) + footer

    # ---------- 便利方法 ----------
    def convert_and_share(self, file_path):
        if not self.token:
            self.login()
        model_id = self.upload_model(file_path)
        self.wait_conversion(model_id)
        return self.create_share(model_id)


def main():
    args = sys.argv[1:]
    if not args:
        print("BIMWing 上传/查询工具")
        print("用法:")
        print("  python3 bimwing_client.py <模型文件路径>        # 上传 + 转码 + 返回分享链接")
        print("  python3 bimwing_client.py list [页码]           # 列出当前账号模型(默认第1页,每页20)")
        print("  python3 bimwing_client.py share <模型id>        # 为已有模型生成分享链接")
        print("  python3 bimwing_client.py preview <模型id>      # 生成可点击的「打开页」(HTML)")
        print("  python3 bimwing_client.py status <模型id>       # 查看模型转码状态")
        sys.exit(1)

    mobile, password = load_credentials()
    if not mobile or not password:
        print("缺少 BIMWing 凭证：请设置环境变量 BIMWING_MOBILE/PASSWORD，或在首次使用时按提示输入账号密码。")
        sys.exit(2)
    client = BimwingClient(mobile, password)
    client.login()

    if args[0] == "list":
        page = 1
        if len(args) >= 2 and args[1].isdigit():
            page = int(args[1])
        print(client.format_models(page))
        return
    if args[0] == "share" and len(args) >= 2:
        url = client.create_share(args[1])
        name = (client.model_status(args[1]).get("fileName") if args[1] else None)
        page = client.make_open_page(url, name)
        print(url)
        print(f"\n[可点击打开页] {page}")
        return
    if args[0] == "preview" and len(args) >= 2:
        # 仅为已有模型生成「打开页」（不会重新上传/转码）
        url = client.create_share(args[1])
        name = client.model_status(args[1]).get("fileName")
        page = client.make_open_page(url, name)
        print(url)
        print(f"\n[可点击打开页] {page}")
        return
    if args[0] == "status" and len(args) >= 2:
        print(json.dumps(client.model_status(args[1]), ensure_ascii=False, indent=2))
        return
    # 否则当作文件路径：上传 + 转码 + 分享
    file_path = args[0]
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        sys.exit(3)
    url = client.convert_and_share(file_path)
    page = client.make_open_page(url, os.path.basename(file_path))
    print("\n=== BIMWing 分享链接 ===")
    print(url)
    print(f"\n[可点击打开页] {page}")


if __name__ == "__main__":
    main()
