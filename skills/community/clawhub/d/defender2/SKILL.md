---
name: defender2
description: Scan npm packages or projects to detect JavaScript malware and Windows filename RLO malware,供应链攻击和恶意包。使用 when: (1) 用户要求扫描npm包安全性 (2) 检测恶意JS代码、PUA字符、可疑Base64编码 (3) 分析package.json依赖和脚本 (4) 识别已知恶意包如os-info-checker-es6变种
---

# defender2 - NPM恶意软件检测

使用内置的 `pua.py` 脚本扫描 npm 包和项目，检测 JavaScript 恶意软件。

## setup
```
pip install rlo-detect
```

## 使用方法

```bash
python skills/defender2/scripts/pua.py <path> [-r] [-v]
```

## 参数

- `path`: 要扫描的路径（文件或目录）
- `-r, --recursive`: 递归扫描子目录
- `-v, --verbose`: 显示详细信息

## example

```bash
# 扫描整个项目
python skills/defender2/scripts/pua.py ./my-project

# 扫描单个package.json
python skills/defender2/scripts/pua.py ./package.json

# 递归扫描node_modules
python skills/defender2/scripts/pua.py ./node_modules --recursive

# rlo malware detect
rlo-detect ./my-project
```

## 检测功能

1. **PUA字符检测** - 检测Unicode私有使用区字符的混淆技术
2. **恶意模式匹配** - 检测eval(atob())、Buffer.from()等危险代码模式
3. **IOC检测** - 识别已知恶意包名、IP、C2地址
4. **Base64解码** - 解码隐藏的可疑代码
5. **持久化技术** - 检测单例锁文件、异常捕获等隐蔽技术
6. **依赖分析** - 检查package.json中的恶意依赖
