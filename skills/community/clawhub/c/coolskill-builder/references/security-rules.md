# 5 层安全校验规则

## L1: 依赖扫描
- 正则提取所有 `import X` / `from X import`，对比白名单
- 扫描 `requirements.txt`, `setup.py`, `pyproject.toml`, `pip install` 字符串，存在即阻断
- 白名单：sys, json, os, re, math, random, datetime, itertools, collections, typing, inspect, hashlib, base64, urllib.request, http.client, socket, ssl, time, uuid, string, warnings, traceback, io, csv, html.parser, pathlib, fnmatch, glob, copy, functools, enum, dataclasses, contextlib, builtins
- 修复：原生代码重写

## L2: 注入与执行检测
- 禁止：`eval(`, `exec(`, `compile(`, `os.system(`, `subprocess.`, `pty.`
- 禁止：`getattr(__builtins__,...)` 动态反射调用危险函数
- 禁止用户输入直接拼接进 SQL/命令/路径
- 文件路径禁止 `../` 或绝对路径写（除非 perms 含 fs）
- 修复：安全等价实现

## L3: 密钥硬编码检测
- 正则扫描：
  - `[a-zA-Z0-9_-]{20,}` 疑似 API Key/Token
  - `(sk-|pk-|AKIA|ghp-|gpt-)[a-zA-Z0-9]+`
  - `(password|passwd|pwd|secret|token|api_key)\s*=\s*['"][^'"]+['"]`
- 发现硬编码 → 阻断
- 修复：改为 `os.environ.get('X')` 并在 perms 中加 env

## L4: 网络边界检测
- 若 perms 无 `net`，但代码含 `urllib`, `http.client`, `socket` → 阻断
- 若 perms 有 `net`，检查 URL 是否为硬编码（应通过参数传入）
- 修复：URL 移入输入参数

## L5: 输出与信息泄露检测
- 禁止直接返回 `traceback.format_exc()` 或 `sys.exc_info()`
- 禁止返回 `os.environ`, `open('/etc/passwd').read()`, 密钥变量
- 修复：统一错误格式 `{'s':'err','e':'internal_error'}`，敏感信息脱敏

## 阻断行为
任一层失败立即停止，不执行后续步骤，不写入 Registry。仅输出修复指令。
