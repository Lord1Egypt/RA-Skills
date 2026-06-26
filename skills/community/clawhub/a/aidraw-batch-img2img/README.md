# AIDraw批量生图自动化工具 - Windows版使用说明

## 简介

这是AIDraw批量生图自动化工具的Windows版本，用于腾讯混元AI平台(timiai.woa.com)的批量图生图自动化。可以自动上传参考图片、生成AI图片并下载到本地。

## 功能特点

- 批量处理多张参考图片
- 每张图片可生成多次（默认4次，可配置）
- 自动下载生成的图片
- 支持自定义关键词
- 自动选择"4K高清"清晰度
- 自动命名保存（原文件名_序号.png）

## Windows系统要求

- Windows 10 或更高版本
- Python 3.8+
- 稳定的网络连接（需能访问腾讯内网timiai.woa.com）

## 安装步骤

### 1. 检查Python版本

打开命令提示符（CMD）或PowerShell，检查Python版本：

```cmd
python --version
```

如果版本低于3.8，请先安装Python 3.8+。

### 2. 安装依赖

使用pip安装所需包：

```cmd
pip install playwright requests
```

如果提示权限问题，可以尝试：

```cmd
pip install --user playwright requests
```

### 3. 安装Playwright浏览器

```cmd
playwright install chromium
```

### 4. 验证安装

```cmd
python -c "import playwright; print('Playwright 安装成功')"
python -c "import requests; print('Requests 安装成功')"
```

## 使用方法

### 方式一：作为WorkBuddy Skill使用

1. 打开WorkBuddy
2. 进入"专家中心"
3. 点击"导入Skill"
4. 选择 `AIDraw-batch-img2img-win.zip` 文件
5. 安装完成后，可以通过对话方式使用

### 方式二：作为独立脚本使用

1. 打开命令提示符（CMD）或PowerShell
2. 进入脚本目录：

```cmd
cd C:\Users\YourName\Desktop\AIDraw批量生图-WIN版
```

3. 使用Python运行：

```cmd
python scripts\batch_img2img.py
```

或者使用PowerShell：

```powershell
python scripts/batch_img2img.py
```

## 配置参数

在 `scripts\batch_img2img.py` 中修改以下参数：

```python
# 源文件夹路径（包含参考图片）
# 注意：Windows路径使用反斜杠 \ 或双反斜杠 \\
source_folder = r"C:\Users\YourName\Desktop\参考图片文件夹"

# 生成关键词（风格描述）
keyword = """你的关键词描述"""

# 每张图片生成的次数
generations_per_image = 4
```

**Windows路径格式说明：**
- 主目录在 `C:\Users\你的用户名\`
- 桌面在 `C:\Users\你的用户名\Desktop\`
- 文档在 `C:\Users\你的用户名\Documents\`
- 使用反斜杠 `\` 或在字符串前加 `r` 原始字符串

## 工作流程

1. 启动脚本
2. 自动打开浏览器并访问 timiai.woa.com
3. 对每张参考图片：
   - 切换到"参考生图"模式
   - 清空旧的参考图片
   - 上传新的参考图片
   - 输入关键词
   - 选择"自适应"比例
   - 选择"4K高清"清晰度
   - 点击生成
   - 等待生成完成
   - 自动下载图片
   - 验证图片完整性
4. 所有图片处理完成后，显示结果统计

## 输出结果

- 图片保存在：`源文件夹名_日期AI`（在源文件夹的上级目录）
- 文件命名：`原文件名_序号.png`
- 示例：`角色A_001.png`、`角色A_002.png`、`角色B_003.png`

## Windows系统注意事项

1. **Python路径**：如果提示找不到python命令，可以使用完整路径：
   ```cmd
   C:\Users\YourName\AppData\Local\Programs\Python\Python38\python.exe scripts\batch_img2img.py
   ```

2. **路径分隔符**：Windows使用反斜杠 `\`，使用 `r""` 原始字符串避免转义问题

3. **防火墙/杀毒软件**：运行时如果被防火墙或杀毒软件阻止，请添加白名单

4. **浏览器窗口**：运行时会打开浏览器窗口，请勿关闭

5. **网络稳定性**：确保网络稳定，避免中断

6. **失败处理**：如果某张图片生成失败，脚本会自动跳过继续下一张

## 常见问题解决

### 问题1：找不到python命令

**解决方法：**
```cmd
# 查看Python安装路径
where python

# 或者使用完整路径
C:\Users\YourName\AppData\Local\Programs\Python\Python38\python.exe scripts\batch_img2img.py
```

### 问题2：pip命令不存在

**解决方法：**
```cmd
# 使用python -m pip
python -m pip install playwright requests

# 或者使用完整路径
C:\Users\YourName\AppData\Local\Programs\Python\Python38\python.exe -m pip install playwright requests
```

### 问题3：playwright install失败

**解决方法：**
```cmd
# 尝试重新安装
playwright install --force chromium

# 或者使用管理员权限运行（以管理员身份打开CMD）
playwright install chromium
```

### 问题4：网络访问timiai失败

**解决方法：**
- 确保已连接到腾讯内网VPN
- 检查防火墙设置
- 尝试在浏览器中手动访问 https://timiai.woa.com
- 检查代理设置

### 问题5：文件编码问题

**解决方法：**
如果遇到编码错误，在脚本开头添加：
```python
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

## 关键词模板

工具内置了多个关键词模板，可在 `references\keyword-templates.md` 中查看：

- 新海诚风格（二次元动画）
- 光影优化（二分色修正）
- 赛博朋克风格
- 水彩画风
- 厚涂插画

## 分享说明

这个工具以Skill形式打包，可以分享给其他WorkBuddy用户。

分享步骤：
1. 发送 `AIDraw-batch-img2img-win.zip` 文件
2. 接收方在WorkBuddy中导入即可使用

## 文件清单

```
AIDraw批量生图-WIN版\
├── SKILL.md                          # Skill主文档
├── scripts\
│   └── batch_img2img.py              # 主执行脚本
├── references\
│   └── keyword-templates.md          # 关键词模板
├── 使用说明-Windows版.md              # 本文件
└── AIDraw-batch-img2img-win.zip      # 打包文件
```

## 快速开始示例

1. 准备参考图片文件夹：`C:\Users\YourName\Desktop\我的图片`
2. 修改脚本配置：
   ```python
   source_folder = r"C:\Users\YourName\Desktop\我的图片"
   generations_per_image = 4
   keyword = "新海诚风格，动画电影摄影质感"
   ```
3. 运行脚本：
   ```cmd
   python scripts\batch_img2img.py
   ```
4. 等待完成，查看结果：`C:\Users\YourName\Desktop\我的图片_0408AI`

## 技术支持

如有问题，请联系工具开发者或在WorkBuddy中反馈。

---

**版本**：1.0 Windows版  
**更新日期**：2026年4月8日  
**适用平台**：Windows 10+ / WorkBuddy

**测试记录：**
- ✅ Windows 10 + Python 3.8.5 测试通过
- ✅ Windows 11 + Python 3.9+ 测试通过
- ✅ 成功批量生成210张图片（42张×5次）
