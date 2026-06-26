// ========== 基础操作 ==========
// 搜索应用商店
export async function searchApps(client, input = {}) {
    const response = await client.request({
        method: 'POST',
        path: '/api/v2/apps/search',
        body: {
            page: input.page ?? 1,
            pageSize: input.pageSize ?? 20,
            name: input.name ?? ''
        }
    });
    const data = response.data;
    if (data.code !== 200) {
        throw new Error(`搜索失败: ${data.code}`);
    }
    return data.data?.items ?? [];
}
// 通过 key 获取应用信息
export async function getAppByKey(client, key) {
    const response = await client.request({
        method: 'GET',
        path: `/api/v2/apps/${key}`
    });
    const data = response.data;
    if (data.code === 200 && data.data) {
        return { data: data.data };
    }
    return null;
}
// 获取 appDetailId（用于安装）
export async function getAppDetailId(client, key, version) {
    const response = await client.request({
        method: 'GET',
        path: `/api/v2/apps/detail/node/${key}/${version}`
    });
    const data = response.data;
    if (data.code === 200 && data.data?.id) {
        return data.data.id;
    }
    return null;
}
// 列出已安装应用
export async function listInstalledApps(client) {
    const response = await client.request({
        method: 'GET',
        path: '/api/v2/apps/installed/list'
    });
    const data = response.data;
    return data.data ?? [];
}
// 搜索已安装应用
export async function searchInstalledApps(client, input = {}) {
    const response = await client.request({
        method: 'POST',
        path: '/api/v2/apps/installed/search',
        body: {
            page: input.page ?? 1,
            pageSize: input.pageSize ?? 20,
            name: input.name ?? ''
        }
    });
    const data = response.data;
    return {
        items: data.data?.items ?? [],
        total: data.data?.total ?? 0
    };
}
// 安装应用
export async function installApp(client, input) {
    if (!input.appDetailId) {
        throw new Error('缺少必需参数: appDetailId');
    }
    if (!input.name) {
        throw new Error('缺少必需参数: name');
    }
    const response = await client.request({
        method: 'POST',
        path: '/api/v2/apps/install',
        body: {
            appDetailId: input.appDetailId,
            name: input.name,
            params: input.params || {}
        }
    });
    const data = response.data;
    return {
        success: data.code === 200,
        message: data.message || '',
        data: data.data
    };
}
// 卸载应用
export async function uninstallApp(client, installId) {
    const response = await client.request({
        method: 'POST',
        path: '/api/v2/apps/installed/op',
        body: {
            installId: Number(installId),
            operate: 'delete'
        }
    });
    const data = response.data;
    return {
        success: data.code === 200,
        message: data.message || ''
    };
}
// ========== 高级操作 ==========
// 一站式安装（自动获取 appDetailId）
export async function installAppByKey(client, key, options = {}) {
    // 获取应用信息
    const appResult = await getAppByKey(client, key);
    if (!appResult || !appResult.data) {
        return {
            success: false,
            message: `未找到应用: ${key}`
        };
    }
    const app = appResult.data;
    const version = options.version || app.versions[0];
    // 获取 appDetailId
    const appDetailId = await getAppDetailId(client, key, version);
    if (!appDetailId) {
        return {
            success: false,
            message: `无法获取 ${key}:${version} 的 appDetailId`
        };
    }
    // 安装
    const name = options.name || key;
    return await installApp(client, {
        appDetailId,
        name,
        params: options.params
    });
}
// ========== 批量操作 ==========
// 批量安装应用
export async function batchInstallApps(client, apps) {
    const result = {
        total: apps.length,
        succeeded: 0,
        failed: 0,
        results: []
    };
    for (const app of apps) {
        const installResult = await installAppByKey(client, app.key, {
            name: app.name,
            version: app.version
        });
        result.results.push({
            item: app.key,
            success: installResult.success,
            message: installResult.message
        });
        if (installResult.success) {
            result.succeeded++;
        }
        else {
            result.failed++;
        }
        // 避免请求过快
        await new Promise(resolve => setTimeout(resolve, 500));
    }
    return result;
}
// 批量卸载应用
export async function batchUninstallApps(client, installIds) {
    const result = {
        total: installIds.length,
        succeeded: 0,
        failed: 0,
        results: []
    };
    for (const id of installIds) {
        const uninstallResult = await uninstallApp(client, id);
        result.results.push({
            item: String(id),
            success: uninstallResult.success,
            message: uninstallResult.message
        });
        if (uninstallResult.success) {
            result.succeeded++;
        }
        else {
            result.failed++;
        }
        await new Promise(resolve => setTimeout(resolve, 500));
    }
    return result;
}
// 按名称批量卸载
export async function batchUninstallByName(client, names) {
    // 获取已安装应用
    const installed = await listInstalledApps(client);
    const nameToId = new Map(installed.map(app => [app.name, app.id]));
    const result = {
        total: names.length,
        succeeded: 0,
        failed: 0,
        results: []
    };
    for (const name of names) {
        const id = nameToId.get(name);
        if (!id) {
            result.results.push({
                item: name,
                success: false,
                message: '未找到该应用'
            });
            result.failed++;
            continue;
        }
        const uninstallResult = await uninstallApp(client, id);
        result.results.push({
            item: name,
            success: uninstallResult.success,
            message: uninstallResult.message
        });
        if (uninstallResult.success) {
            result.succeeded++;
        }
        else {
            result.failed++;
        }
        await new Promise(resolve => setTimeout(resolve, 500));
    }
    return result;
}
//# sourceMappingURL=appstore.js.map