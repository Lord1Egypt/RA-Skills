# ClawHub Publish Notes

## Local Test

```bash
cd clawhub-skills/cryptorank-radar
python3 scripts/run_skill.py --mode radar --lang zh --limit 5 --output json
python3 scripts/run_skill.py --mode funding --lang zh --limit 5 --output markdown
```

## Package

```bash
cd clawhub-skills/cryptorank-radar
python3 scripts/package_skill.py
```

打包后会生成：

```text
clawhub-skills/cryptorank-radar/dist/cryptorank-radar-1.0.0.zip
```

## Upload Suggestions

- 确认 `SKILL.md` frontmatter 中的 `description` 使用英文
- 确认 `version` 遵循 semver
- 确认 skill 目录内已经包含 `SKILL.md`、`_meta.json`、`LICENSE.txt`
- 如果平台支持本地测试，先运行对应的 test / validate 命令
- 如果平台要求 zip 上传，直接使用 `dist/` 下的打包产物

## Notes

- 当前 skill 默认使用中文输出
- 该 skill 走的是 CryptoRank 免费层抓取逻辑
- 如需接入官方 API，可后续扩展新的 wrapper 版本
