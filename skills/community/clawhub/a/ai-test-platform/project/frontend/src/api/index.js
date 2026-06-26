import api from './request'

// ==================== 授权相关 ====================

// 验证授权码
export const verifyAuth = (authCode) => {
  return api.post('/auth/verify', {
    auth_code: authCode
  })
}

// ==================== AI生成相关 ====================

// 生成测试用例
export const generateTestCase = (data) => {
  return api.post('/generate/case', data)
}

// 生成API脚本
export const generateApiScript = (data) => {
  return api.post('/generate/api', data)
}

// 生成UI脚本
export const generateUiScript = (data) => {
  return api.post('/generate/ui', data)
}

// 查询任务进度
export const getTaskProgress = (taskId) => {
  return api.get(`/generate/progress/${taskId}`)
}

// ==================== API测试相关 ====================

// 创建API脚本
export const createApiScript = (data) => {
  return api.post('/api/script', data)
}

// 获取API脚本列表
export const getApiScriptList = () => {
  return api.get('/api/script/list')
}

// 获取API脚本详情
export const getApiScriptDetail = (id) => {
  return api.get(`/api/script/${id}`)
}

// 更新API脚本
export const updateApiScript = (id, data) => {
  return api.put(`/api/script/${id}`, data)
}

// 删除API脚本
export const deleteApiScript = (id) => {
  return api.delete(`/api/script/${id}`)
}

// 调试API脚本
export const debugApiScript = (id, environment) => {
  return api.post(`/api/script/${id}/debug`, null, {
    params: { environment }
  })
}

// 配置环境
export const configureEnvironment = (data) => {
  return api.post('/api/environment', data)
}

// 获取环境配置
export const getEnvironment = (name) => {
  return api.get(`/api/environment/${name}`)
}

// ==================== UI测试相关 ====================

// 创建UI脚本
export const createUiScript = (data) => {
  return api.post('/ui/script', data)
}

// 获取UI脚本列表
export const getUiScriptList = () => {
  return api.get('/ui/script/list')
}

// 获取UI脚本详情
export const getUiScriptDetail = (id) => {
  return api.get(`/ui/script/${id}`)
}

// 更新UI脚本
export const updateUiScript = (id, data) => {
  return api.put(`/ui/script/${id}`, data)
}

// 删除UI脚本
export const deleteUiScript = (id) => {
  return api.delete(`/ui/script/${id}`)
}

// 配置浏览器
export const configureBrowser = (scriptId, data) => {
  return api.post('/ui/browser/config', { script_id: scriptId, ...data })
}

// ==================== 测试执行相关 ====================

// 执行单个脚本
export const executeScript = (data) => {
  return api.post('/execute/run', data)
}

// 批量执行脚本
export const executeBatch = (data) => {
  return api.post('/execute/batch', data)
}

// 查询执行进度
export const getExecuteProgress = (taskId) => {
  return api.get(`/execute/progress/${taskId}`)
}

// 获取执行记录
export const getExecuteRecords = (params) => {
  return api.get('/execute/records', { params })
}

// 获取执行记录详情
export const getExecuteRecordDetail = (id) => {
  return api.get(`/execute/record/${id}`)
}

// ==================== 测试报告相关 ====================

// 生成测试报告
export const generateReport = (data) => {
  return api.post('/report/generate', data)
}

// 获取报告列表
export const getReportList = (params) => {
  return api.get('/report/list', { params })
}

// 获取报告详情
export const getReportDetail = (id) => {
  return api.get(`/report/${id}`)
}

// 导出报告
export const exportReport = (data) => {
  return api.post('/report/export', data, {
    responseType: 'blob'
  })
}

// 生成AI分析
export const generateAiAnalysis = (data) => {
  return api.post('/report/ai-analysis', data)
}

// 删除报告
export const deleteReport = (id) => {
  return api.delete(`/report/${id}`)
}

// ==================== 执行管理相关 ====================

// 创建执行器
export const createExecutor = (data) => {
  return api.post('/execution/executor', data)
}

// 获取执行器列表
export const getExecutorList = (params) => {
  return api.get('/execution/executor/list', { params })
}

// 获取执行器详情
export const getExecutorDetail = (id) => {
  return api.get(`/execution/executor/${id}`)
}

// 删除执行器
export const deleteExecutor = (id) => {
  return api.delete(`/execution/executor/${id}`)
}

// 执行器心跳
export const executorHeartbeat = (id, currentLoad) => {
  return api.post(`/execution/executor/${id}/heartbeat`, null, {
    params: { current_load: currentLoad }
  })
}

// 调度任务
export const scheduleTask = (data) => {
  return api.post('/execution/task/schedule', data)
}

// 获取任务列表
export const getTaskList = (params) => {
  return api.get('/execution/task/list', { params })
}

// 取消任务
export const cancelTask = (taskId) => {
  return api.post('/execution/task/cancel', { task_id: taskId })
}

// 获取执行统计
export const getExecutionStats = () => {
  return api.get('/execution/stats')
}

// 自动调度
export const autoSchedule = () => {
  return api.post('/execution/auto-schedule')
}

// 清理过期任务
export const cleanupTasks = (hours) => {
  return api.post('/execution/cleanup', null, {
    params: { hours }
  })
}

// ==================== 系统管理相关 ====================

// 创建AI模型配置
export const createAiModelConfig = (data) => {
  return api.post('/system/ai-model', data)
}

// 获取AI模型配置列表
export const getAiModelConfigList = (params) => {
  return api.get('/system/ai-model/list', { params })
}

// 获取默认AI模型配置
export const getDefaultAiModelConfig = () => {
  return api.get('/system/ai-model/default')
}

// 获取AI模型配置详情
export const getAiModelConfigDetail = (id) => {
  return api.get(`/system/ai-model/${id}`)
}

// 更新AI模型配置
export const updateAiModelConfig = (id, data) => {
  return api.put(`/system/ai-model/${id}`, data)
}

// 删除AI模型配置
export const deleteAiModelConfig = (id) => {
  return api.delete(`/system/ai-model/${id}`)
}

// 测试AI模型配置
export const testAiModelConfig = (id) => {
  return api.post(`/system/ai-model/${id}/test`)
}

// 创建测试环境
export const createEnvironment = (data) => {
  return api.post('/system/environment', data)
}

// 获取测试环境列表
export const getEnvironmentList = (params) => {
  return api.get('/system/environment/list', { params })
}

// 获取默认测试环境
export const getDefaultEnvironment = () => {
  return api.get('/system/environment/default')
}

// 获取测试环境详情
export const getEnvironmentDetail = (id) => {
  return api.get(`/system/environment/${id}`)
}

// 更新测试环境
export const updateEnvironment = (id, data) => {
  return api.put(`/system/environment/${id}`, data)
}

// 删除测试环境
export const deleteEnvironment = (id) => {
  return api.delete(`/system/environment/${id}`)
}

// 获取操作日志列表
export const getOperationLogList = (params) => {
  return api.get('/system/log/list', { params })
}

// 创建数据备份
export const createBackup = (data) => {
  return api.post('/system/backup', data)
}

// 获取备份列表
export const getBackupList = (params) => {
  return api.get('/system/backup/list', { params })
}

// 获取备份详情
export const getBackupDetail = (id) => {
  return api.get(`/system/backup/${id}`)
}

// 删除备份
export const deleteBackup = (id) => {
  return api.delete(`/system/backup/${id}`)
}

// 恢复备份
export const restoreBackup = (data) => {
  return api.post('/system/backup/restore', data)
}
