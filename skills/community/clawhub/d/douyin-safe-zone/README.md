# Douyin Safe Zone

使用可调整的参考安全区规划抖音 9:16 视频、图文和 3:4 封面，并可生成透明 PNG 参考叠层。尺寸是项目经验值，不是抖音官方规则或兼容保证；最终以当前发布预览为准。

## 运行叠层生成器

依赖 Python 3 和 Pillow：

```bash
python3 scripts/create_safe_zone_overlay.py --profile douyin-playback-reference --output /tmp/douyin-guide.png
python3 scripts/create_safe_zone_overlay.py --profile douyin-cover-3x4 --output /tmp/douyin-cover-guide.png
```

支持 `--top`、`--right`、`--bottom`、`--left` 覆盖默认值。叠层只用于设计时参考，导出前应隐藏或删除。

## 内容

- [Skill 使用说明](SKILL.md)
- [MIT No Attribution 许可](LICENSE)
- [来源记录](SOURCE-ORIGIN.md)

自测：`python3 scripts/self_test.py`。生成器依赖 Pillow；需要其他输出格式时请自行转换，并检查透明度是否保留。
