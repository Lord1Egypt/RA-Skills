# Failure Modes

- raw materials 请求缺少具体本地路径时，不要直接路由到 `ingest-materials`；先要求补路径。
- lifecycle、打包或提交请求缺少 `library_id` / `package_plan_id` 等前提时，明确指出缺失字段，并回退到前置阶段。
- 请求同时混合多个阶段且证据不足时，优先选择最早缺失阶段。
- 用户已经明确要求某个阶段时，不要为了“完整流程”强行改写为整条主线。
