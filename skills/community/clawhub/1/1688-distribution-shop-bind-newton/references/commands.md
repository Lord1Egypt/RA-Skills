# 命令参考

## bind_shop —— 绑店流程主入口

```bash
# 启动绑店（未指定平台时，返回 ISV 工具列表供选择）
python3 cli.py bind_shop --action start

# 启动绑店（指定平台）
python3 cli.py bind_shop --action start --channel douyin --app-key YOUR_APP_KEY

# 用户选择平台后，继续流程
python3 cli.py bind_shop --action start --user-input "抖音"

# 浏览器操作完成后，继续流程
python3 cli.py bind_shop --action continue --channel douyin --app-key YOUR_APP_KEY

# 查询当前流程状态
python3 cli.py bind_shop --action query --channel douyin --app-key YOUR_APP_KEY

# 关闭绑店流程
python3 cli.py bind_shop --action close --channel douyin --app-key YOUR_APP_KEY
```

## shop_info —— 查询店铺和工具信息

```bash
# 查询当前用户的 ISV 工具和绑定店铺
python3 cli.py shop_info
```

## browser —— 浏览器操作（调试用）

```bash
# 在牛顿浏览器中打开 URL
python3 cli.py browser --action open --url "https://..." --wait-login

# 关闭浏览器
python3 cli.py browser --action close

# 获取浏览器状态
python3 cli.py browser --action status
```
