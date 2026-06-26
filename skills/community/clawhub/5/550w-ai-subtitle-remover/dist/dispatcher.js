"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.invoke = invoke;
const types_1 = require("./types");
const credential_manager_1 = require("./credential-manager");
const api_client_1 = require("./api-client");
const upload_video_1 = require("./actions/upload-video");
const submit_task_1 = require("./actions/submit-task");
const task_detail_1 = require("./actions/task-detail");
const task_list_1 = require("./actions/task-list");
const query_credits_1 = require("./actions/query-credits");
const workflow_engine_1 = require("./workflow-engine");
async function invoke(request) {
    const credentialManager = new credential_manager_1.CredentialManager();
    if (!credentialManager.isConfigured()) {
        return credentialManager.getGuideMessage();
    }
    const validActions = ["uploadVideo", "submitTask", "taskDetail", "taskList", "queryCredits", "workflow"];
    if (!validActions.includes(request.action)) {
        return { code: types_1.ErrorCode.INVALID_PARAMS, message: `不支持的 action: ${request.action}` };
    }
    const credential = credentialManager.get();
    const client = new api_client_1.ApiClient(credential);
    switch (request.action) {
        case "uploadVideo": return (0, upload_video_1.uploadVideo)(request.params, client);
        case "submitTask": return (0, submit_task_1.submitTask)(request.params, client);
        case "taskDetail": return (0, task_detail_1.taskDetail)(request.params, client);
        case "taskList": return (0, task_list_1.taskList)(request.params, client);
        case "queryCredits": return (0, query_credits_1.queryCredits)(request.params, client);
        case "workflow": return (0, workflow_engine_1.executeWorkflow)(request.params, client);
        default: return { code: types_1.ErrorCode.INVALID_PARAMS, message: `不支持的 action: ${request.action}` };
    }
}
//# sourceMappingURL=dispatcher.js.map