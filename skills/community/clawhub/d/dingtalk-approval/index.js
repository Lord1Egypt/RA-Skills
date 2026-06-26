// 钉钉 OA 审批插件 - 适配 OpenClaw 2026.3.2+ 版本
// 版本：2.3.1 - 待发布版（统一元数据、补全文档与工具清单）

let config = {};

// 获取应用访问令牌
async function getDingtalkToken() {
    const res = await fetch("https://api.dingtalk.com/v1.0/oauth2/accessToken", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ appKey: config.appKey, appSecret: config.appSecret })
    });
    const data = await res.json();
    return data.accessToken;
}

// 脱敏配置信息（用于日志输出）
function sanitizeConfig(cfg) {
    if (!cfg) return '{}';
    return JSON.stringify({
        dingtalkUserId: cfg.dingtalkUserId ? `${cfg.dingtalkUserId.substring(0, 4)}***` : 'undefined',
        appKey: cfg.appKey ? `${cfg.appKey.substring(0, 6)}***` : 'undefined',
        appSecret: cfg.appSecret ? '***REDACTED***' : 'undefined'
    });
}

// 脱敏附件信息（隐藏 fileId）
function sanitizeAttachment(att) {
    if (!att) return null;
    return {
        fileName: att.fileName || '未知文件',
        fileSize: att.fileSize || 0,
        fileType: att.fileType || 'unknown',
        // 隐藏敏感的 fileId 和 spaceId
        fileId: '[REDACTED]',
        spaceId: '[REDACTED]'
    };
}

// 脱敏处理审批详情（隐藏敏感字段）
function sanitizeInstance(instance) {
    if (!instance) return null;
    
    const sanitized = { ...instance };
    
    // 脱敏附件字段
    if (sanitized.form_component_values) {
        sanitized.form_component_values = sanitized.form_component_values.map(comp => {
            if (comp.component_name === '附件' || comp.name === '附件') {
                const value = comp.component_value || comp.value;
                if (Array.isArray(value)) {
                    const safeAttachments = value.map(att => sanitizeAttachment(att));
                    return {
                        ...comp,
                        component_value: safeAttachments,
                        value: safeAttachments
                    };
                }
            }
            return comp;
        });
    }
    
    return sanitized;
}

function register(api) {
    // OpenClaw 2026.3.8 从 api.config.plugins.entries.dingtalk-approval.config 读取插件配置
    config = api.config?.plugins?.entries?.["dingtalk-approval"]?.config || {};
    
    console.log("[dingtalk-approval] 插件注册中...");
    console.log("[dingtalk-approval] 配置内容（已脱敏）:", sanitizeConfig(config));
    
    if (!config.dingtalkUserId || !config.appKey || !config.appSecret) {
        console.error("[dingtalk-approval] 配置不完整！请在 openclaw.json 中配置 dingtalkUserId、appKey 和 appSecret");
        // 即使配置不完整，也继续注册工具，但工具会返回错误信息
    } else {
        console.log("[dingtalk-approval] 配置加载成功，用户 ID:", `${config.dingtalkUserId.substring(0, 4)}***`);
    }
    
    // 工具 1: 查询待办任务
    api.registerTool({
        name: "get_pending_tasks",
        description: "查询我的 OA 审批待办任务列表。在执行同意或拒绝操作前，必须先调用此工具获取任务详情和任务 ID。",
        parameters: {
            type: "object",
            properties: {},
            additionalProperties: false
        },
        execute: async (toolCallId, args) => {
            // 配置检查
            if (!config.appKey || !config.appSecret) {
                return "❌ 配置错误：插件尚未配置，请联系管理员设置 appKey 和 appSecret";
            }
            
            try {
                const token = await getDingtalkToken();
                
                if (!token) {
                    return "❌ 认证失败：无法获取访问令牌，请检查 appKey 和 appSecret 是否正确";
                }
                
                const res = await fetch(`https://oapi.dingtalk.com/topapi/process/workrecord/task/query?access_token=${token}`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        userid: config.dingtalkUserId,
                        offset: 0,
                        count: 50,
                        status: 0
                    })
                });
                const data = await res.json();
                
                if (!data.result || !data.result.list) {
                    return "❌ 查询失败：API 返回异常，请稍后重试";
                }
                
                const tasks = data.result.list;
                if (tasks.length === 0) {
                    return "✅ 当前没有待办单据";
                }
                
                return tasks.map((t, i) => `${i + 1}. ${t.title} (任务 ID: ${t.task_id})`).join("\n");
            } catch (error) {
                console.error("[dingtalk-approval] 查询待办失败:", error.message);
                return "❌ 查询失败：网络异常，请稍后重试";
            }
        }
    });
    
    // 工具 2: 查询审批单详情
    api.registerTool({
        name: "get_task_details",
        description: "查询 OA 审批单的详细信息，包括申请人、申请内容、审批流程等。需要先调用 get_pending_tasks 获取 task_id。",
        parameters: {
            type: "object",
            properties: {
                task_id: { 
                    type: "string", 
                    description: "待办任务的唯一 ID（从 get_pending_tasks 获取）" 
                }
            },
            required: ["task_id"],
            additionalProperties: false
        },
        execute: async (toolCallId, args) => {
            // 配置检查
            if (!config.appKey || !config.appSecret) {
                return "❌ 配置错误：插件尚未配置，请联系管理员设置 appKey 和 appSecret";
            }
            
            try {
                const token = await getDingtalkToken();
                
                if (!token) {
                    return "❌ 认证失败：无法获取访问令牌";
                }
                
                // 先查询任务获取 instance_id
                const queryRes = await fetch(`https://oapi.dingtalk.com/topapi/process/workrecord/task/query?access_token=${token}`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        userid: config.dingtalkUserId,
                        offset: 0,
                        count: 50,
                        status: 0
                    })
                });
                const queryData = await queryRes.json();
                const tasks = queryData.result?.list || [];
                const task = tasks.find(t => String(t.task_id) === String(args.task_id));
                
                if (!task) {
                    return `❌ 未找到任务 ID ${args.task_id}，请确认任务 ID 正确`;
                }
                
                // 获取审批实例详情
                const detailRes = await fetch(`https://oapi.dingtalk.com/topapi/processinstance/get?access_token=${token}`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        process_instance_id: task.instance_id
                    })
                });
                const detailData = await detailRes.json();
                
                if (detailData.errcode !== 0) {
                    return `❌ 查询失败：${detailData.errmsg ? detailData.errmsg : 'API 返回错误'}`;
                }
                
                // 脱敏处理
                const instance = sanitizeInstance(detailData.process_instance);
                
                // 构建详情信息
                let result = [];
                result.push(`📋 **审批单详情**`);
                result.push(``);
                result.push(`**单据标题**: ${instance.title || task.title || '未知'}`);
                result.push(`**申请人**: ${instance.creator_name || instance.creatorNick || '未知'}`);
                result.push(`**申请时间**: ${instance.create_time ? new Date(instance.create_time).toLocaleString('zh-CN') : '未知'}`);
                result.push(`**当前状态**: ${instance.status === 2 ? '审批中' : instance.status === 3 ? '已通过' : instance.status === 4 ? '已拒绝' : '审批中'}`);
                result.push(`**审批类型**: ${instance.process_code_name || instance.process_code || task.title || '未知'}`);
                result.push(``);
                
                // 表单内容
                if (instance.form_component_values && instance.form_component_values.length > 0) {
                    result.push(`📝 **申请内容**:`);
                    for (const comp of instance.form_component_values) {
                        const name = comp.component_name || comp.name || '未知';
                        let value = comp.component_value || comp.value || '未知';
                        
                        // 附件字段特殊处理（脱敏 fileId 和 spaceId）
                        if (name === '附件') {
                            if (Array.isArray(value)) {
                                const attCount = value.length;
                                const totalSize = value.reduce((sum, att) => sum + (att.fileSize || 0), 0);
                                value = `${attCount} 个附件 (共 ${(totalSize / 1024).toFixed(1)} KB)`;
                            } else if (value && typeof value === 'string' && value.includes('fileId')) {
                                // 如果是字符串且包含 fileId，说明是 JSON 字符串
                                value = '附件（已脱敏）';
                            } else if (value === 'null' || value === null) {
                                value = '无附件';
                            }
                        }
                        
                        if (name && value) {
                            result.push(`- ${name}: ${value}`);
                        }
                    }
                    result.push(``);
                }
                
                // 审批流程
                if (instance.operation_records && instance.operation_records.length > 0) {
                    result.push(`🔄 **审批流程**:`);
                    for (const op of instance.operation_records) {
                        const action = op.result === 'agree' ? '✅ 同意' : op.result === 'refuse' ? '❌ 拒绝' : '⏳ 待审批';
                        const time = op.time ? new Date(op.time).toLocaleString('zh-CN') : '';
                        const userName = op.operate_user_name || op.user_name || op.nick || '系统';
                        result.push(`- ${op.result ? action : '⏳ 待审批'} | ${userName} | ${time}`);
                    }
                    result.push(``);
                }
                
                // 备注
                if (instance.remark || task.remark) {
                    result.push(`💬 **备注**: ${instance.remark || task.remark}`);
                }
                
                return result.join('\n');
            } catch (error) {
                console.error("[dingtalk-approval] 查询详情失败:", error.message);
                return "❌ 查询失败：网络异常，请稍后重试";
            }
        }
    });
    
    // 工具 3: 执行审批操作
    api.registerTool({
        name: "execute_approval_task",
        description: "执行 OA 审批的同意或拒绝操作。必须先调用 get_pending_tasks 获取 task_id 后才能使用。",
        parameters: {
            type: "object",
            properties: {
                task_id: { 
                    type: "string", 
                    description: "待办任务的唯一 ID（从 get_pending_tasks 获取）" 
                },
                action: { 
                    type: "string", 
                    enum: ["AGREE", "REFUSE"], 
                    description: "审批动作：AGREE(同意) 或 REFUSE(拒绝)" 
                },
                remark: { 
                    type: "string", 
                    description: "审批意见/备注（可选）" 
                }
            },
            required: ["task_id", "action"],
            additionalProperties: false
        },
        execute: async (toolCallId, args) => {
            // 配置检查
            if (!config.appKey || !config.appSecret) {
                return "❌ 配置错误：插件尚未配置，请联系管理员设置 appKey 和 appSecret";
            }
            
            try {
                const token = await getDingtalkToken();
                
                if (!token) {
                    return "❌ 认证失败：无法获取访问令牌";
                }
                
                // 先查询任务获取 instance_id
                const queryRes = await fetch(`https://oapi.dingtalk.com/topapi/process/workrecord/task/query?access_token=${token}`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        userid: config.dingtalkUserId,
                        offset: 0,
                        count: 50,
                        status: 0
                    })
                });
                const queryData = await queryRes.json();
                const tasks = queryData.result?.list || [];
                const task = tasks.find(t => String(t.task_id) === String(args.task_id));
                
                if (!task) {
                    return `❌ 未找到任务 ID ${args.task_id}，请确认任务 ID 正确`;
                }
                
                // 执行审批
                const executeRes = await fetch("https://api.dingtalk.com/v1.0/workflow/processInstances/execute", {
                    method: "POST",
                    headers: { 
                        "Content-Type": "application/json",
                        "x-acs-dingtalk-access-token": token
                    },
                    body: JSON.stringify({
                        processInstanceId: task.instance_id,
                        taskId: args.task_id,
                        actionerUserId: config.dingtalkUserId,
                        result: args.action === "AGREE" ? "agree" : "refuse",
                        remark: args.remark || (args.action === "AGREE" ? "同意" : "拒绝")
                    })
                });
                const executeData = await executeRes.json();
                
                if (executeRes.ok && (executeData.success || executeData.code === "OK" || !executeData.code)) {
                    return `✅ 审批成功！已将任务 "${task.title}" 标记为${args.action === "AGREE" ? "同意" : "拒绝"}`;
                }
                
                return `❌ 审批失败：${executeData.errmsg || '请稍后重试'}`;
            } catch (error) {
                console.error("[dingtalk-approval] 执行审批失败:", error.message);
                return "❌ 执行失败：网络异常，请稍后重试";
            }
        }
    });
    
    // 工具 4: 查询假期余额
    api.registerTool({
        name: "get_vacation_balance",
        description: "查询我的假期余额（年假、病假等）。需要应用开通 qyapi_holiday_readonly 权限。",
        parameters: {
            type: "object",
            properties: {},
            additionalProperties: false
        },
        execute: async (toolCallId, args) => {
            // 配置检查
            if (!config.appKey || !config.appSecret) {
                return "❌ 配置错误：插件尚未配置，请联系管理员设置 appKey 和 appSecret";
            }
            
            try {
                const token = await getDingtalkToken();
                
                if (!token) {
                    return "❌ 认证失败：无法获取访问令牌";
                }
                
                // 查询假期类型列表
                const typeRes = await fetch(`https://oapi.dingtalk.com/topapi/attendance/vacation/type/list?access_token=${token}`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        op_userid: config.dingtalkUserId,
                        userid: config.dingtalkUserId
                    })
                });
                const typeData = await typeRes.json();
                
                if (typeData.errcode === 88 && typeData.sub_code === "60011") {
                    return "❌ 权限不足：应用尚未开通假期查询权限（qyapi_holiday_readonly）。\n\n请在钉钉开放平台中为当前应用申请该权限后重试。";
                }
                
                if (typeData.errcode !== 0) {
                    return `❌ 查询失败：${typeData.errmsg || '请稍后重试'}`;
                }
                
                const vacationTypes = typeData.result?.vacation_type_list || [];
                
                if (vacationTypes.length === 0) {
                    return "ℹ️ 未找到假期类型配置";
                }
                
                // 查询每个假期类型的余额
                let result = [];
                for (const vt of vacationTypes) {
                    const balanceRes = await fetch(`https://oapi.dingtalk.com/topapi/attendance/vacation/quota/list?access_token=${token}`, {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                            op_userid: config.dingtalkUserId,
                            userid: config.dingtalkUserId,
                            vacation_type_id: vt.vacation_type_id
                        })
                    });
                    const balanceData = await balanceRes.json();
                    
                    if (balanceData.errcode === 0 && balanceData.result?.quota_list) {
                        const quota = balanceData.result.quota_list[0];
                        if (quota) {
                            result.push({
                                name: vt.vacation_name,
                                total: quota.quota_num,
                                used: quota.used_num,
                                left: quota.quota_num - quota.used_num,
                                unit: quota.quota_unit === "day" ? "天" : "小时"
                            });
                        }
                    }
                }
                
                if (result.length === 0) {
                    return "ℹ️ 暂无假期余额数据";
                }
                
                return result.map(r => `${r.name}: ${r.left}${r.unit} (总${r.total}${r.unit}, 已用${r.used}${r.unit})`).join("\n");
            } catch (error) {
                console.error("[dingtalk-approval] 查询假期失败:", error.message);
                return "❌ 查询失败：网络异常，请稍后重试";
            }
        }
    });
    
    console.log("[dingtalk-approval] 插件注册完成（安全加固版）");
}

module.exports = { register };
