# config.ini 配置说明

## 文件位置

首次运行 `convert2docx.ps1` 或 `convert2docx.bat` 后，自动生成在 skill 根目录：

```
~/.workbuddy/skills/convert2docx/config.ini
```

## 格式

```ini
[pandoc]
path=C:\Program Files\Pandoc\pandoc.exe

[reference]
path=C:\Users\YourName\Documents\reference.docx
```

| 字段 | 说明 | 是否必填 |
|------|------|----------|
| `[pandoc] path` | pandoc.exe 完整路径 | 是 |
| `[reference] path` | reference.docx 完整路径 | 是 |

## 修改方法

**方法一：直接编辑**

用记事本打开 `config.ini`，改完保存即可。

**方法二：删掉重新生成**

删除 `config.ini`，下次运行时重新提示输入。

**方法三：命令行覆盖**

```powershell
# 单次运行指定不同的 reference，不改配置文件
.\convert2docx.ps1 input.md -ReferencePath "D:\other\reference.docx"

# 单次运行指定不同的 pandoc
.\convert2docx.ps1 input.md -PandocPath "D:\tools\pandoc.exe"
```

## 注意事项

1. **路径含空格**：直接写，不需要加引号
2. **路径分隔符**：用反斜杠 `\` 或正斜杠 `/` 都可以
3. **reference.docx 必须存在**：路径无效会报错并提示重新配置
4. **编码**：文件用 UTF-8 保存（脚本写入时已是 UTF-8）

## 多份配置

目前只支持全局一份 `config.ini`。若需要按项目用不同的 reference，建议：
- 命令行用 `-ReferencePath` 参数指定
- 或在项目目录下放一个快捷方式，参数里写死路径
