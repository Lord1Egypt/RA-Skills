# dimens-manager 画布章节 命令映射

## 命令与接口

| 命令 | 作用 | 接口 |
| --- | --- | --- |
| `canvas create` | 创建项目画布菜单资源 | `POST /app/mul/project/:projectId/sheet/create` |
| `canvas info` | 获取画布详情 | `GET /app/canvas/:teamId/:projectId/info` |
| `canvas validate` | 本地校验画布 JSON 是否满足可渲染保存结构 | 本地命令，不请求接口 |
| `canvas save` | 保存画布图数据 | `POST /app/canvas/:teamId/:projectId/save` |
| `canvas versions` | 获取版本列表 | `POST /app/canvas/:teamId/:projectId/versions` |
| `canvas version` | 获取指定版本快照 | `GET /app/canvas/:teamId/:projectId/version` |
| `canvas restore` | 恢复指定版本 | `POST /app/canvas/:teamId/:projectId/restore` |
| `canvas resource-list` | 查看我的组件资源 | `GET /app/canvas/:teamId/resource/mine` |
| `canvas resource-save` | 保存我的组件资源 | `POST /app/canvas/:teamId/resource/mine` |
| `canvas resource-delete` | 删除我的组件资源 | `POST /app/canvas/:teamId/resource/mine/delete` |
| `canvas resource-publish` | 发布资源到市场 | `POST /app/canvas/:teamId/resource/mine/publish` |
| `canvas resource-market` | 查看资源市场 | `GET /app/canvas/:teamId/resource/market` |

## 常用链路

```bash
dimens-cli canvas create --team-id TEAM1 --project-id PROJ1 --name 业务流程画布
dimens-cli canvas info canvas_1 --team-id TEAM1 --project-id PROJ1
dimens-cli canvas validate --file ./canvas.json
dimens-cli canvas save canvas_1 --team-id TEAM1 --project-id PROJ1 --base-version 1 --file ./canvas.json --summary AI生成业务工作流
dimens-cli canvas info canvas_1 --team-id TEAM1 --project-id PROJ1
dimens-cli canvas versions canvas_1 --team-id TEAM1 --project-id PROJ1
```

```bash
dimens-cli canvas versions canvas_1 --team-id TEAM1 --project-id PROJ1
dimens-cli canvas restore canvas_1 --team-id TEAM1 --project-id PROJ1 --version 2
```
