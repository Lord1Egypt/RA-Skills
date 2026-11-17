# Docker Compose 单机部署流程

## 目录约定

```text
/opt/app-name/
  docker-compose.yml
  .env
  data/
  config/
  logs/
```

## 上线步骤

1. 确认端口未被占用。
2. 创建部署目录。
3. 上传代码或部署包。
4. 创建 `.env`，不要提交真实密码。
5. 执行 `docker compose up -d --build`。
6. 检查健康接口和容器日志。

## 验证命令

```bash
docker compose ps
docker compose logs --tail=100 app
curl -fsS http://127.0.0.1:18088/healthz
```

## 回滚策略

- 保留上一个镜像 tag 或上一个发布目录。
- 数据库迁移必须可重复执行。
- SQLite 文件升级前先备份。

## 注意事项

- 数据目录必须挂载到宿主机。
- 不要把 Redis 或 MySQL 作为默认依赖，除非业务确实需要。
- 对外端口使用五位数端口时，需要同步检查云安全组和系统防火墙。
