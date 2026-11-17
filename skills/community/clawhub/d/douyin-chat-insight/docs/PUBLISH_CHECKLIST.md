# 发布检查清单

版本目标：**v0.1.3**（稳固可公开）

## A. 运行与体验（发布阻塞）

1. [ ] `python3 scripts/doctor.py` → `RESULT: READY`
2. [ ] `python3 -m unittest discover -s tests -v` 全绿
3. [ ] `python3 scripts/setup.py --check --json` → `needs_bailian_appkey: false`
4. [ ] fixture 最短路径：inventory → `--conv 1` → 可打开 `latest.html`
5. [ ] 真实导出（可选但推荐）：深挖后 HTML/MD/JSON **无** `/Users` `/home` `/Volumes`
6. [ ] `--person` 无 `--conv` → exit 2 + 打印概况
7. [ ] 缺文件 / 坏 formats / 空导出 → 中文错误、无 Traceback
8. [ ] README 最短路径与真实入口一致（未上 ClawHub 前 git clone 为真入口）

## B. 仓库洁净

9. [ ] 无 cookie / token / sessionid / 私钥
10. [ ] 无本机私有绝对路径进 `docs/examples` 与 fixtures
11. [ ] `.gitignore` 含 `output/`、`config.yaml`、`__pycache__/`
12. [ ] LICENSE = MIT；SECURITY.md 存在

## C. 发布动作（需你点头）

13. [ ] GitHub 建库 + push（visibility 你定）
14. [ ] tag `v0.1.3`
15. [ ] （可选）Gitee 镜像
16. [ ] （可选）`clawhub skill publish` + 全新目录 install 验收
17. [ ] 本机 `link_shared_skill.py douyin-chat-insight --apply`
18. [ ] （可选）脱敏演示内容（GTM）— 需用户授权真实案例

## D. 定位自检

- 一句话：Chat → Insight，不是爬群工具
- 赚钱路径不写进 skill 主流程（见 GTM）
- Agent 状态机：无 `--conv` 不深挖
