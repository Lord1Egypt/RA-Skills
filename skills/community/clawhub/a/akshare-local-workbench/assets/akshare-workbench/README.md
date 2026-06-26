# AKShare Data SaaS

一个前后端分离的 AKShare 数据提取工作台。用户可以在网页选择金融指标、填写参数、执行提取，并将结果预览或导出为 Excel、CSV、JSON。

## 功能

- 指标分级：资产大类、市场/主题、数据族、具体 AKShare 接口。
- 白名单调用：后端只允许调用 `backend/app/catalog/indicators.yaml` 中登记的 AKShare 函数。
- 临时任务：内存中只保留当前任务数据；刷新页面、新任务、手动清理或 TTL 到期会清除残留。
- 数据预览：前端展示提取结果前 100 行，并显示行数、列数和字段。
- 多格式导出：支持 `xlsx`、`csv`、`json`。

## 本地启动

### 通过 Codex/OpenClaw Skill 启动

安装 skill 后可在项目根目录执行：

```bash
python3 ~/.codex/skills/akshare-local-workbench/scripts/workbench_ctl.py doctor
python3 ~/.codex/skills/akshare-local-workbench/scripts/workbench_ctl.py setup
python3 ~/.codex/skills/akshare-local-workbench/scripts/workbench_ctl.py start
```

如果不在项目根目录，追加 `--root /path/to/project`。该方式会使用更保守的数据源访问策略，普通「提取」优先复用本地缓存，「强制刷新」才会重新请求数据源，以降低东方财富等源站的访问受限概率。

### 后端

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

后端默认运行在 `http://127.0.0.1:8000`，接口文档在 `http://127.0.0.1:8000/docs`。

### 前端

```bash
cd frontend
npm install
npm run dev
```

前端默认运行在 `http://127.0.0.1:5173`，Vite 会把 `/api` 代理到后端。

## 指标维护

新增指标时编辑 `backend/app/catalog/indicators.yaml`：

- `id`：前端和 API 使用的唯一标识。
- `level1` / `level2` / `level3`：指标分级。
- `ak_function`：AKShare 函数名。
- `params`：动态表单参数，支持 `string`、`date`、`select`、`integer`、`number`、`boolean`。
- `docs_url`：AKShare 官方文档链接。

登记后无需改前端，页面会自动渲染指标和参数表单。

## 测试

```bash
cd backend
pytest

cd ../frontend
npm run build
```
