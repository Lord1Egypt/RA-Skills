# boss-cli — BOSS 直聘查询工具

**by Barry**

> 本工具仅用于查询 BOSS 直聘职位，不涉及任何投递/打招呼/聊天操作。

## 功能

- 🔍 搜索职位（城市/薪资/经验/行业/规模/融资阶段）
- ⭐ 个性化推荐
- 📋 职位详情查看
- 📊 CSV/JSON 导出
- 📮 查看已投递记录
- 👤 查看个人资料

## 安装

```bash
uv tool install kabi-boss-cli
pipx install kabi-boss-cli
pip install kabi-boss-cli --user
```

## 登录

```bash
boss login   # 自动从浏览器提取 cookie
boss login --qrcode   # 扫码登录
boss status   # 检查状态
```

## 常用命令

```bash
boss search "golang" --city 杭州 --salary 20-30K
boss recommend
boss export "Python" -n 50 -o jobs.csv
boss cities
```

## License

Apache-2.0
