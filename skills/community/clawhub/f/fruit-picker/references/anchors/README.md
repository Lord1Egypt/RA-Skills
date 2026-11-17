# anchors/ 说明

本目录图片均为 AI 生成示意图，非实拍；长期用实拍逐步替换（身份类优先）。

- `howto-*`：给用户的动作与拍摄指引。什么时机发哪张，见 [../output-guide.md](../output-guide.md) 第 7 节。
- `anchor-*`：多档同图对比，Agent 判档参照，用户问档位时也可发出；只用于档位相对关系，不作品种鉴定或真伪依据。

## 读取图片

优先读取本目录的同名文件。如果安装来源只提供文本、没有附带图片，则从下面的固定地址读取，把 `<文件名>` 换成参考文档中给出的完整文件名：

```text
https://raw.githubusercontent.com/Ezra-Y/fruit-picker/main/fruit-picker/references/anchors/<文件名>
```

本地文件和远程文件都不可用时，不根据文件名猜测图中内容。

刺尖/果壳色度与西瓜纹理不设肉眼锚点，分别由本 skill 的 `scripts/color_lab.py` 和 `scripts/watermelon_texture.py` 计算。
