# BossSkill 客户端发行说明

为了避免核心源码泄露，不要把本私有开发仓库直接发给客户安装。

正确交付方式：

1. 私有开发仓库保留完整核心源码，仅内部维护使用。
2. 服务器 `/opt/booskill-core` 部署核心能力。
3. 客户安装客户端发行包，只包含：
   - 授权校验
   - 免费版基础客户/团队/任务记录
   - 简单 Web 控制台
   - 云端核心调用客户端
   - manifest / 文档
4. 商业高级命令通过 `https://bt.fanfan.la/api/core/run` 调用云端核心。
5. 隐私默认值：授权校验只发送授权码、设备标识和功能名；云端商业命令默认只发送当次命令参数，不上传本地 SQLite 数据库。

生成客户端发行包：

```powershell
python scripts\build_client_release.py --output dist\booskill-client
```

客户安装 `dist/booskill-client`，不要安装本开发仓库。

如需临时调试本地核心，可以设置：

```powershell
$env:BOOSKILL_CORE_MODE="local"
```

这个模式只允许内部开发使用，不用于客户交付。
