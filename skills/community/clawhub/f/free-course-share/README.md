# free-course-share 1.1.5-full

免费课程/证书分享素材工作流：筛课、截图拼图、证书敏感信息打码、3:4 封面和文案草稿。

## 默认行为

- 不添加固定账号水印。
- 不自动加入推广或 CTA。
- 不生成或发布短链。
- 不执行自动发布、定时发布或置顶评论。

这些动作都必须由用户针对本次任务明确确认，且默认关闭。封面的 `--cta` 只有显式传参才启用。

## 安装依赖

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pillow==12.1.0 numpy==2.3.5 \
  opencv-python-headless==4.13.0.92 pytesseract==0.3.13
```

另需安装 Tesseract 与 `chi_sim` 中文语言包。

## 快速使用

```bash
# 两列拼图
python3 scripts/stitch.py two-col 图1.png 图2.png 图3.png -o 拼图.png

# OCR 定位打码
python3 scripts/redact.py \
  --src 证书.png --text "姓名" --out 证书-打码.png

# OCR 不可靠时，将文本精确映射到源图坐标
python3 scripts/redact.py \
  --src 证书.png \
  --text "姓名" \
  --text-box "姓名=100,80,260,130" \
  --out 证书-打码.png

# 生成无 CTA 的竖版封面
python3 scripts/cover_vertical.py \
  --out 封面.png --theme dark \
  --title "课程标题" --body 拼图.png
```

## redact.py 关键保证

- 所有坐标严格验证，非法、反向或越界坐标立即失败。
- `--text-box TEXT=x1,y1,x2,y2` 精确关联文本和坐标；`TEXT` 也必须通过 `--text` 声明。
- 未命中文本默认 fail-closed。
- target 匹配分低于 `0.85` 默认退出非零，不写源图或目标图成功输出。
- manifest 的 `targets` 数组记录每个目标的状态、得分、阈值、映射和输出路径。
- `--allow-low-score-targets` 只允许显式跳过低分目标，不保存低分目标。
- 验证目录默认权限 0700、文件 0600；默认不落未打码裁剪。

完整流程、安全边界和参数说明见 `SKILL.md`。

## 测试

```bash
python3 -m unittest discover -s tests -v
```

## License

MIT
