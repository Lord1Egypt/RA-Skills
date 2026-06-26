#!/usr/bin/env node

/**
 * 单体 Node.js 脚本：触发图片渲染
 * 功能：不依赖 Puppeteer，直接调用接口实现：
 * 1. 获取设计 levelId
 * 2. 触发智能视角生成 (asyncmatch)
 * 3. 轮询相机就绪状态 (status)
 * 4. 提交离线渲染任务 (submit)
 *
 * 使用方式：node trigger-render.js --obsDesignId=xxx --xToken=yyy --maxAttempts=10 --interval=3 --cameraType=1
 */
// --- 配置与常量 ---

/** 酷家乐基础地址 */
const BASE_URL = 'https://oauth.kujiale.com';

/** 获取设计详情接口 */
const DESIGN_GET_API_PATH = '/oauth2/openapi/ai-design-skill/factory/api/design/get';
/** 触发智能视角匹配接口 */
const ASYNC_MATCH_API_PATH = '/oauth2/openapi/ai-design-skill/auto-camera';
/** 查询相机状态接口 */
const CAMERA_STATUS_API_PATH = '/oauth2/openapi/ai-design-skill/auto-camera/status';
/** 提交离线渲染任务接口 */
const OFFLINE_RENDER_SUBMIT_API_PATH = '/oauth2/openapi/ai-design-skill/render/submit';

/** 相机类型：普通图 */
const CAMERA_TYPE_NORMAL = 1;
/** 相机类型：全景图 */
const CAMERA_TYPE_PANORAMA = 2;
/** 离线渲染快照类型：普通图1k 1024*576 */
const SNAPSHOT_TYPE_ID_NORMAL = 720;
/** 离线渲染快照类型：全景图2k */
const SNAPSHOT_TYPE_ID_PANORAMA = 745;

/** 默认灯光样式 ID */
const DEFAULT_OBS_LIGHT_STYLE_ID = '3FO4K4VMXE4K';
/** 默认外景 ID */
const DEFAULT_OBS_BACKGROUND_ID = '3FO4K4AXQ5MW';

const ROOM_CONFIGS = [
  {
    names: ['客餐厅', '客厅', '餐厅', '起居室'],
  },
  {
    names: [
      '主卧',
      '衣帽间',
      '步入式衣柜',
      '次卧',
      '客卧',
      '女孩房',
      '男孩房',
      '老人房',
      '儿童房',
      '卧室',
      '保姆房',
    ],
  },
  {
    names: ['厨房', '中厨', '西厨'],
  },
  {
    names: ['书房', '多功能室', '电竞房'],
  },
  {
    names: ['卫生间', '主卫', '次卫'],
  },
  {
    names: ['阳台', '生活阳台'],
  },
  {
    names: ['未命名', '其他'],
  },
]

// --- 工具函数 ---

/**
 * 解析命令行参数
 * @returns {Record<string, string>}
 */
function parseArgs() {
  const args = {};
  process.argv.slice(2).forEach((val) => {
    if (val.startsWith('--')) {
      const [key, value] = val.split('=');
      args[key.slice(2)] = value;
    }
  });
  return args;
}

/**
 * 睡眠函数
 * @param {number} ms 毫秒
 */
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function main() {
  const { obsDesignId, xToken, maxAttempts, interval, cameraType } = parseArgs();
  if (!obsDesignId || !xToken) {
    console.error('Usage: node trigger-render.js --obsDesignId=xxx --xToken=yyy [--maxAttempts=10] [--interval=3] [--cameraType=1|2]');
    process.exit(1);
  }

  /**
 * 封装 Fetch 请求，自动注入鉴权 Header、解析 URL 参数、响应解析、解密以及 Body 处理
 * @param {object} param0
 * @param {string} param0.url 请求地址
 * @param {object} [param0.options={}] fetch 配置
 * @param {object} [param0.params=null] URL 查询参数对象
 * @returns {Promise<any>} 解析后的 JSON 对象或解密后的对象
 */
  async function request({ url, options = {}, params = null }) {
    const finalUrl = new URL(url);
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        finalUrl.searchParams.set(key, value);
      });
    }

    const headers = {
      'accept': 'application/json',
      'Authorization': `Bearer ${xToken}`,
      ...(options.headers || {})
    };

    const fetchOptions = {
      ...options,
      headers,
    };

    if (options.body && typeof options.body === 'object') {
      fetchOptions.body = JSON.stringify(options.body);
    }

    const response = await fetch(finalUrl.toString(), fetchOptions);
    const json = await response.json();

    if (!response.ok) {
      throw new Error(`Request Failed. Status: ${response.status}. URL: ${finalUrl.toString()}. Body: ${json}`);
    }

    try {
      if (typeof json === 'object') {
        return json;
      } else if (typeof json === 'string') {
        return JSON.parse(json);
      } else {
        return json;
      }
    } catch (e) {
      return text;
    }
  }

  // 默认配置
  const pollingMaxAttempts = maxAttempts ? Number(maxAttempts) : 10;
  const pollingIntervalMs = interval ? Number(interval) * 1000 : 3000;
  // 相机类型过滤
  const targetCameraType = cameraType ? Number(cameraType) : null;

  try {
    console.log(`Starting trigger render for designId: ${obsDesignId}`);

    // --- 第一步：获取 levelId ---
    console.log('[Step 1] Fetching design details...');
    const designRes = await request({
      url: `${BASE_URL}${DESIGN_GET_API_PATH}`,
      options: { method: 'GET' },
      params: { obsDesignId }
    });
    const levelId = designRes.d?.levelId;
    if (!levelId) {
      throw new Error(`Failed to get levelId from design info: ${JSON.stringify(designRes)}`);
    }
    console.log(`[Step 1] Got levelId: ${levelId}`);

    // --- 第二步：触发智能视角生成 (asyncmatch) ---
    console.log('[Step 2] Triggering async camera matching...');
    const triggerMatch = async (cameraTypeId) => {
      const params = {
        obsdesignid: obsDesignId,
        levelid: levelId,
        refresh: 1,
        filter: 1,
        deduplication: true,
        cameratypeid: cameraTypeId,
        bizprefix: 'design-factory'
      };
      return await request({
        url: `${BASE_URL}${ASYNC_MATCH_API_PATH}`,
        options: { method: 'POST' },
        params
      });
    };

    const needTriggerCameraTypes = {};
    if (targetCameraType === CAMERA_TYPE_NORMAL) {
      needTriggerCameraTypes[CAMERA_TYPE_NORMAL] = true;
    } else if (targetCameraType === CAMERA_TYPE_PANORAMA) {
      needTriggerCameraTypes[CAMERA_TYPE_PANORAMA] = true;
    } else {
      needTriggerCameraTypes[CAMERA_TYPE_NORMAL] = true;
      needTriggerCameraTypes[CAMERA_TYPE_PANORAMA] = true;
    }

    const triggerRes = await Promise.all([
      needTriggerCameraTypes[CAMERA_TYPE_NORMAL] ? triggerMatch(CAMERA_TYPE_NORMAL) : Promise.resolve(false),
      needTriggerCameraTypes[CAMERA_TYPE_PANORAMA] ? triggerMatch(CAMERA_TYPE_PANORAMA) : Promise.resolve(false)
    ]);

    // --- 第三步：轮询相机状态 ---

    /**
     * 轮询相机状态直到就绪
     * @param {number} cameraTypeId
     */
    async function waitForCameraReady(cameraTypeId) {
      /**const url = `${BASE_URL}${CAMERA_STATUS_API_PATH}`; **/
	  const url = 'https://www.kujiale.com/rcs/interface/api/c/common/autocamera/secure/status';
      const params = { cameratypeid: cameraTypeId, obsdesignid: obsDesignId, levelid: levelId, bizprefix: 'design-factory' };

      for (let attempt = 1; attempt <= pollingMaxAttempts; attempt++) {
        console.log(`[Polling] Checking status for cameraTypeId=${cameraTypeId} (Attempt ${attempt}/${pollingMaxAttempts})...`);
        const decryptedPayload = await request({
          url,
          options: {
            method: 'GET',
          },
          params
        });

        const status = Number(decryptedPayload.status);
        console.log(`[Polling] cameraTypeId=${cameraTypeId}, status=${status}`);

        if (status === 2) {
          return extractShotType3List(decryptedPayload);
        }

        if (status === -1 || status === 3) {
          throw new Error(`Camera status error for type ${cameraTypeId}: status=${status}`);
        }

        if (attempt < pollingMaxAttempts) {
          await sleep(pollingIntervalMs);
        }
      }

      throw new Error(`Wait for camera type ${cameraTypeId} ready failed after ${pollingMaxAttempts} attempts.`);
    }

    /** 从响应中提取 shotType 为 3 的视角列表 */
    function extractShotType3List(payload) {
      const roomIdAutoCameraMap = payload.autoCameraResult?.roomIdAutoCameraMap || {};
      const merged = Object.values(roomIdAutoCameraMap).flatMap((shots) => (Array.isArray(shots) ? shots : []));
      return merged.filter((shot) => Number(shot.shotType) === 3);
    }

    console.log('[Step 3] Waiting for cameras to be ready...');
    const [normalResult, panoramaResult] = await Promise.all([
      triggerRes[0] ? waitForCameraReady(CAMERA_TYPE_NORMAL) : Promise.resolve([]),
      triggerRes[1] ? waitForCameraReady(CAMERA_TYPE_PANORAMA) : Promise.resolve([])
    ]);

    // --- 第四步：提交渲染任务 ---

    /**
     * 按照业务规则筛选视角
     * @param {any[]} shotList 原始视角列表
     * @param {number} maxPerRoom 每个房间最多张数
     * @param {number} maxPerType 每类房间最多张数
     * @param {number} maxTotal 总计最多张数
     */
    function filterShots(shotList, maxPerRoom, maxPerType, maxTotal) {
      if (!shotList || shotList.length === 0) return [];

      /** 获取房间所属的分类索引 */
      const getCategoryIndex = (roomName) => {
        const index = ROOM_CONFIGS.findIndex(cfg => cfg.names.includes(roomName));
        return index !== -1 ? index : ROOM_CONFIGS.length;
      };

      // 先按分类索引分组
      const categorizedShots = [];
      for (let i = 0; i <= ROOM_CONFIGS.length; i++) {
        categorizedShots[i] = [];
      }

      for (const shot of shotList) {
        const categoryIndex = getCategoryIndex(shot.roomName);
        categorizedShots[categoryIndex].push(shot);
      }

      const filtered = [];
      const roomUsedCount = {};
      const typeUsedCount = {};

      // 按 ROOM_CONFIGS 顺序遍历
      for (let i = 0; i <= ROOM_CONFIGS.length; i++) {
        for (const shot of categorizedShots[i]) {
          if (filtered.length >= maxTotal) break;

          const roomId = String(shot.roomId);
          const categoryIndex = i;

          roomUsedCount[roomId] = roomUsedCount[roomId] || 0;
          typeUsedCount[categoryIndex] = typeUsedCount[categoryIndex] || 0;

          // 检查房间限制和分类限制
          if (roomUsedCount[roomId] < maxPerRoom && typeUsedCount[categoryIndex] < maxPerType) {
            filtered.push(shot);
            roomUsedCount[roomId]++;
            typeUsedCount[categoryIndex]++;
          }
        }
        if (filtered.length >= maxTotal) break;
      }
      return filtered;
    }

    /**
     * 提交渲染任务
     * @param {any[]} shotType3List 视角数据
     * @param {number} snapshotTypeId 快照类型
     */
    async function submitTasks(shotType3List, snapshotTypeId) {
      if (!shotType3List || shotType3List.length === 0) {
        console.log(`[Step 4] No shotType3 views to submit for snapshotTypeId=${snapshotTypeId}, skipping.`);
        return [];
      }

      const payload = shotType3List.map(shot => {
        const cameraData = shot.cameraData;
        return {
          snapshotTypeId,
          obsLightStyleId: DEFAULT_OBS_LIGHT_STYLE_ID,
          obsBackgroundId: DEFAULT_OBS_BACKGROUND_ID,
          cameraId: `${shot.roomId}-${shot.id}`,
          cameraInfo: {
            camPos: cameraData.camPos,
            cameraTypeId: shot.cameraTypeId,
            clippingNear: cameraData.clippingNear,
            lookAtPos: cameraData.lookAtPos,
            hfov: cameraData.hfov,
          },
          sceneBizData: {
            roomId: String(shot.roomId),
            obsDesignId: obsDesignId,
            levelId: String(levelId),
          },
        };
      });

      console.log(`[Step 4] Submitting ${payload.length} tasks for snapshotTypeId=${snapshotTypeId}...`);
      const submitRes = await request({
        url: `${BASE_URL}${OFFLINE_RENDER_SUBMIT_API_PATH}`,
        options: {
          method: 'POST',
          body: payload,
          headers: {
            'content-type': 'application/json',
          }
        }
      });

      if (String(submitRes.c ?? '') !== '0') {
        throw new Error(`Submit failed: ${submitRes.m}`);
      }
      return (submitRes.d || []).map(t => t.taskId).filter(id => !!id);
    }

    const [normalTaskIds, panoramaTaskIds] = await Promise.all([
      submitTasks(filterShots(normalResult, 2, 3, 6), SNAPSHOT_TYPE_ID_NORMAL),
      submitTasks(filterShots(panoramaResult, 1, 2, 4), SNAPSHOT_TYPE_ID_PANORAMA)
    ]);

    console.log('\nSuccess!');
    console.log('------------------------------------');
    console.log('Normal Task IDs:', normalTaskIds);
    console.log('Panorama Task IDs:', panoramaTaskIds);
    console.log('------------------------------------');

  } catch (error) {
    console.error('\nError occurred:');
    console.error(error.message);
    process.exit(1);
  }
}

main();
