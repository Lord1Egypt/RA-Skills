# 每日讲读书库 Daily-reading library

每本书一个自包含文件夹，按书本身的章节顺序存放每期产物：

| 书 | 文件夹 | 每期路径 |
|---|---|---|
| 资治通鉴 | `tongjian/` | `volVVV/epNNN/` |
| 大唐西域记 | `xuanzang/` | `volVV/epNNN/` |
| 罗摩衍那 | `ramayana/` | `bookBB/epNNN/` |
| 禅宗公案 | `zen-koan/` | `epNNN-<slug>/` |

每期：`lecture.md`（讲稿，相对链接引用图和音频）、`map.png`/`image.png`（图）、`voice.mp3`（语音）、`read.txt`（朗读稿）。
每本书：`book.json`（按期序的清单）、`index.md`（目录）、`export/`（导出结果）。

- 归档一期：`python3 library.py add --book <book> --episode N [--chapter C | --slug S] --title … --lecture … --image … --audio … --read …`
- 查缺：`python3 library.py status --book <book>`
- 导出整本：`python3 export_book.py <book> [--embed-images] [--embed-audio] [--from N --to M]` → `<book>/export/<book>.md` + `<book>.html`

## 安装 Install

脚本源文件在本仓库的 `daily-library/`。各每日讲读 skill 的命令默认调用绝对路径 `/workspace/library/library.py` 和 `/workspace/library/export_book.py`。安装时把本目录复制或软链接到 `/workspace/library/`：

```bash
ln -sfn /path/to/YumSkills/daily-library /workspace/library
# 或：cp -a daily-library/. /workspace/library/
```

`export_book.py` 生成 HTML 需要 Python 包 `markdown`（`pip install markdown`）。Markdown 导出不依赖它。
