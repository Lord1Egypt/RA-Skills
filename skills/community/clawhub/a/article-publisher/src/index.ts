import { getAdapter, getAllAdapters } from './adapters/index.js';
import { PlatformName, PLATFORMS, ArticleContent, LoginStatus, PublishResult, ToolResult } from './types/index.js';
import { checkAndInstall, quickCheck } from './lib/auto-install.js';

/**
 * 工具定义
 * 
 * check_environment - 检查环境并自动安装依赖（首次使用时调用）
 * login_platform - 登录指定平台
 * check_login_status - 检查登录状态
 * logout_platform - 退出登录
 * publish_article - 发布文章到指定平台
 * publish_to_all - 发布到所有已登录平台
 * list_platforms - 列出所有平台及状态
 */

/**
 * 检查环境并自动安装依赖
 * 这是首次使用时应该调用的工具
 */
export async function check_environment(): Promise<ToolResult> {
  try {
    const result = await checkAndInstall();
    
    if (result.ready) {
      return {
        result: `✅ ${result.message}\n\n环境已就绪，可以使用以下功能：\n- login_platform: 登录平台\n- publish_article: 发布文章\n- list_platforms: 查看所有平台`,
        data: { ready: true }
      };
    } else {
      return {
        result: `⚠️ ${result.message}`,
        data: { ready: false }
      };
    }
  } catch (error) {
    return {
      result: `环境检查失败: ${error instanceof Error ? error.message : String(error)}\n\n请手动运行以下命令安装依赖：\n1. npm install --registry=https://registry.npmmirror.com\n2. npm run install:browser:cn`,
      data: { ready: false }
    };
  }
}

/**
 * 登录平台
 */
export async function login_platform(params: { platform: PlatformName }): Promise<ToolResult> {
  const { platform } = params;
  
  if (!PLATFORMS[platform]) {
    return {
      result: `不支持的平台: ${platform}。支持的平台有: ${Object.keys(PLATFORMS).join(', ')}`,
    };
  }

  try {
    const adapter = getAdapter(platform);
    const message = await adapter.openLoginPage();
    
    return {
      result: message,
      data: {
        platform,
        status: 'waiting_for_login',
        loginUrl: PLATFORMS[platform].loginUrl,
      },
    };
  } catch (error) {
    return {
      result: `登录失败: ${error instanceof Error ? error.message : String(error)}`,
    };
  }
}

/**
 * 等待登录完成
 */
export async function wait_for_login(params: { platform: PlatformName; timeout?: number }): Promise<ToolResult> {
  const { platform, timeout = 120000 } = params;
  
  try {
    const adapter = getAdapter(platform);
    const success = await adapter.waitForLogin(timeout);
    
    if (success) {
      return {
        result: `${PLATFORMS[platform].displayName}登录成功！登录状态已保存，下次使用无需重新登录。`,
        data: { platform, status: 'logged_in' },
      };
    } else {
      return {
        result: `${PLATFORMS[platform].displayName}登录超时，请重试。`,
        data: { platform, status: 'login_timeout' },
      };
    }
  } catch (error) {
    return {
      result: `等待登录失败: ${error instanceof Error ? error.message : String(error)}`,
    };
  }
}

/**
 * 检查登录状态
 */
export async function check_login_status(params: { platform?: PlatformName }): Promise<ToolResult> {
  const { platform } = params;
  
  if (platform) {
    if (!PLATFORMS[platform]) {
      return {
        result: `不支持的平台: ${platform}`,
      };
    }

    try {
      const adapter = getAdapter(platform);
      const isLoggedIn = await adapter.checkLoginStatus();
      const cookieInfo = await new (await import('./lib/cookie-manager.js')).CookieManager(platform).getCookieInfo();
      
      const status: LoginStatus = {
        platform,
        isLoggedIn,
        lastLoginTime: cookieInfo?.createdAt,
        expiresAt: cookieInfo?.expiresAt,
      };

      return {
        result: isLoggedIn
          ? `${PLATFORMS[platform].displayName}已登录。登录时间: ${status.lastLoginTime?.toLocaleString()}，过期时间: ${status.expiresAt?.toLocaleString()}`
          : `${PLATFORMS[platform].displayName}未登录或登录已过期，请先登录。`,
        data: status,
      };
    } catch (error) {
      return {
        result: `检查登录状态失败: ${error instanceof Error ? error.message : String(error)}`,
      };
    }
  } else {
    const statuses: LoginStatus[] = [];
    const adapters = getAllAdapters();
    
    for (const adapter of adapters) {
      try {
        const isLoggedIn = await adapter.checkLoginStatus();
        const cookieInfo = await new (await import('./lib/cookie-manager.js')).CookieManager(adapter.getPlatformName()).getCookieInfo();
        
        statuses.push({
          platform: adapter.getPlatformName(),
          isLoggedIn,
          lastLoginTime: cookieInfo?.createdAt,
          expiresAt: cookieInfo?.expiresAt,
        });
      } catch (error) {
        statuses.push({
          platform: adapter.getPlatformName(),
          isLoggedIn: false,
        });
      }
    }

    const loggedIn = statuses.filter(s => s.isLoggedIn);
    const notLoggedIn = statuses.filter(s => !s.isLoggedIn);

    let message = '登录状态汇总:\n';
    if (loggedIn.length > 0) {
      message += `\n已登录平台: ${loggedIn.map(s => PLATFORMS[s.platform].displayName).join('、')}`;
    }
    if (notLoggedIn.length > 0) {
      message += `\n未登录平台: ${notLoggedIn.map(s => PLATFORMS[s.platform].displayName).join('、')}`;
    }

    return {
      result: message,
      data: statuses,
    };
  }
}

/**
 * 退出登录
 */
export async function logout_platform(params: { platform: PlatformName }): Promise<ToolResult> {
  const { platform } = params;
  
  if (!PLATFORMS[platform]) {
    return {
      result: `不支持的平台: ${platform}`,
    };
  }

  try {
    const adapter = getAdapter(platform);
    await adapter.logout();
    
    return {
      result: `${PLATFORMS[platform].displayName}已退出登录，登录状态已清除。`,
      data: { platform, status: 'logged_out' },
    };
  } catch (error) {
    return {
      result: `退出登录失败: ${error instanceof Error ? error.message : String(error)}`,
    };
  }
}

/**
 * 发布文章
 */
export async function publish_article(params: {
  platform: PlatformName;
  title: string;
  content: string;
  coverImage?: string;
  tags?: string[];
  summary?: string;
  category?: string;
  testMode?: boolean;
}): Promise<ToolResult> {
  const { platform, title, content, coverImage, tags, summary, category, testMode } = params;
  
  if (!PLATFORMS[platform]) {
    return {
      result: `不支持的平台: ${platform}`,
    };
  }

  if (!title || !content) {
    return {
      result: '标题和内容不能为空',
    };
  }

  try {
    const adapter = getAdapter(platform);
    const article: ArticleContent = { title, content, coverImage, tags, summary, category };
    const result: PublishResult = await adapter.publish(article, testMode);
    
    if (result.success) {
      if (testMode) {
        return {
          result: `测试模式：文章《${title}》已填写到${PLATFORMS[platform].displayName}，未发布。`,
          data: result,
        };
      }
      return {
        result: `文章《${title}》已成功发布到${PLATFORMS[platform].displayName}！${result.url ? `\n文章链接: ${result.url}` : ''}`,
        data: result,
      };
    } else {
      return {
        result: `发布失败: ${result.message}${result.error ? `\n错误: ${result.error}` : ''}`,
        data: result,
      };
    }
  } catch (error) {
    return {
      result: `发布失败: ${error instanceof Error ? error.message : String(error)}`,
    };
  }
}

/**
 * 发布到所有已登录平台
 */
export async function publish_to_all(params: {
  title: string;
  content: string;
  coverImage?: string;
  tags?: string[];
  summary?: string;
  category?: string;
  testMode?: boolean;
}): Promise<ToolResult> {
  const { title, content, coverImage, tags, summary, category, testMode } = params;
  
  if (!title || !content) {
    return {
      result: '标题和内容不能为空',
    };
  }

  const article: ArticleContent = { title, content, coverImage, tags, summary, category };
  const adapters = getAllAdapters();
  const results: PublishResult[] = [];

  for (const adapter of adapters) {
    try {
      const isLoggedIn = await adapter.checkLoginStatus();
      if (isLoggedIn) {
        const result = await adapter.publish(article, testMode);
        results.push(result);
      }
    } catch (error) {
      results.push({
        success: false,
        platform: adapter.getPlatformName(),
        message: '发布失败',
        error: error instanceof Error ? error.message : String(error),
      });
    }
  }

  const successCount = results.filter(r => r.success).length;
  const failCount = results.filter(r => !r.success).length;

  let message = testMode 
    ? `测试模式：文章《${title}》已填写完成！\n`
    : `文章《${title}》发布完成！\n`;
  message += `成功: ${successCount}个平台\n`;
  message += `失败: ${failCount}个平台\n`;

  for (const result of results) {
    const platformName = PLATFORMS[result.platform].displayName;
    if (result.success) {
      if (testMode) {
        message += `\n✅ ${platformName}: 已填写${result.url ? ` - ${result.url}` : ''}`;
      } else {
        message += `\n✅ ${platformName}: 发布成功${result.url ? ` - ${result.url}` : ''}`;
      }
    } else {
      message += `\n❌ ${platformName}: ${result.message}`;
    }
  }

  return {
    result: message,
    data: results,
  };
}

/**
 * 列出所有平台
 */
export async function list_platforms(): Promise<ToolResult> {
  const adapters = getAllAdapters();
  const platformList: Array<{
    name: string;
    displayName: string;
    isLoggedIn: boolean;
  }> = [];

  for (const adapter of adapters) {
    try {
      const isLoggedIn = await adapter.checkLoginStatus();
      platformList.push({
        name: adapter.getPlatformName(),
        displayName: adapter.getDisplayName(),
        isLoggedIn,
      });
    } catch {
      platformList.push({
        name: adapter.getPlatformName(),
        displayName: adapter.getDisplayName(),
        isLoggedIn: false,
      });
    }
  }

  let message = '支持的平台列表:\n\n';
  for (const platform of platformList) {
    const status = platform.isLoggedIn ? '✅ 已登录' : '❌ 未登录';
    message += `${platform.displayName} (${platform.name}): ${status}\n`;
  }

  return {
    result: message,
    data: platformList,
  };
}

/**
 * 获取平台支持的分类选项
 * OpenClaw 可以调用此工具获取分类列表，然后根据文章内容分析选择合适的分类
 */
export async function get_category_options(params: { platform: PlatformName }): Promise<ToolResult> {
  const { platform } = params;
  
  if (!PLATFORMS[platform]) {
    return {
      result: `不支持的平台: ${platform}`,
    };
  }

  // 各平台支持的分类列表
  // 注意：这些分类可能随平台更新而变化，建议定期更新
  const categoryMap: Record<string, { categories: string[]; format: string; example: string }> = {
    baijiahao: {
      categories: [
        '科技/互联网',
        '科技/数码',
        '科技/手机',
        '科技/电脑',
        '财经/股票',
        '财经/基金',
        '财经/理财',
        '娱乐/明星',
        '娱乐/电影',
        '娱乐/音乐',
        '体育/足球',
        '体育/篮球',
        '体育/健身',
        '教育/考试',
        '教育/留学',
        '教育/职场',
        '汽车/评测',
        '汽车/导购',
        '美食/菜谱',
        '美食/探店',
        '旅游/国内游',
        '旅游/出境游',
        '时尚/穿搭',
        '时尚/美妆',
        '游戏/手游',
        '游戏/端游',
        '游戏/主机',
        '健康/养生',
        '健康/医疗',
        '育儿/早教',
        '育儿/亲子',
        '历史/历史故事',
        '历史/人物',
        '文化/传统文化',
        '文化/艺术',
        '社会/民生',
        '社会/热点',
        '国际/国际新闻',
        '国际/军事',
      ],
      format: '一级分类/二级分类',
      example: '科技/互联网',
    },
    toutiao: {
      categories: [
        '科技',
        '财经',
        '娱乐',
        '体育',
        '教育',
        '汽车',
        '美食',
        '旅游',
        '时尚',
        '游戏',
        '健康',
        '育儿',
        '历史',
        '文化',
        '社会',
        '国际',
      ],
      format: '单级分类',
      example: '科技',
    },
    zhihu: {
      categories: [
        '科技',
        '科学',
        '互联网',
        '编程',
        '人工智能',
        '心理学',
        '经济学',
        '金融',
        '法律',
        '教育',
        '职业发展',
        '生活',
        '文化',
        '艺术',
        '历史',
        '体育',
        '游戏',
        '汽车',
        '美食',
        '旅行',
        '摄影',
        '时尚',
        '健康',
        '情感',
      ],
      format: '单级分类',
      example: '科技',
    },
    bilibili: {
      categories: [
        '动画',
        '游戏',
        '科技',
        '数码',
        '汽车',
        '生活',
        '美食',
        '时尚',
        '娱乐',
        '音乐',
        '舞蹈',
        '影视',
        '知识',
        '教育',
        '运动',
        '动物',
        '鬼畜',
        '国创',
      ],
      format: '单级分类',
      example: '科技',
    },
    xiaohongshu: {
      categories: [
        '穿搭',
        '美妆',
        '护肤',
        '美食',
        '旅行',
        '健身',
        '家居',
        '母婴',
        '教育',
        '职场',
        '情感',
        '宠物',
        '摄影',
        '艺术',
        '数码',
        '汽车',
      ],
      format: '单级分类',
      example: '穿搭',
    },
  };

  const categoryInfo = categoryMap[platform];
  
  if (!categoryInfo) {
    return {
      result: `暂未配置 ${PLATFORMS[platform].displayName} 的分类列表，请手动传入分类参数`,
      data: { platform, categories: [], format: 'unknown' },
    };
  }

  let message = `${PLATFORMS[platform].displayName} 支持的分类选项:\n\n`;
  message += `分类格式: ${categoryInfo.format}\n`;
  message += `示例: ${categoryInfo.example}\n\n`;
  message += `支持的分类:\n`;
  
  // 按字母/拼音排序显示
  const sortedCategories = [...categoryInfo.categories].sort();
  for (const cat of sortedCategories) {
    message += `  - ${cat}\n`;
  }

  message += `\n提示: 请根据文章标题和内容，选择最合适的分类。`;
  message += `\n如果文章内容涉及多个领域，请选择最主要的一个分类。`;

  return {
    result: message,
    data: {
      platform,
      categories: categoryInfo.categories,
      format: categoryInfo.format,
      example: categoryInfo.example,
    },
  };
}

/**
 * 导出所有工具
 */
export default {
  tools: {
    check_environment: {
      description: '检查环境依赖并自动安装（首次使用时必须调用此工具）。会自动检测并安装 npm 依赖和 Playwright 浏览器。',
      parameters: {},
      execute: check_environment,
    },
    login_platform: {
      description: '登录指定平台，打开浏览器让用户扫码登录',
      parameters: {
        platform: {
          type: 'string',
          description: '平台名称，可选值: zhihu, bilibili, baijiahao, toutiao, xiaohongshu',
          required: true,
        },
      },
      execute: login_platform,
    },
    wait_for_login: {
      description: '等待用户完成扫码登录',
      parameters: {
        platform: {
          type: 'string',
          description: '平台名称',
          required: true,
        },
        timeout: {
          type: 'number',
          description: '超时时间（毫秒），默认120000',
          required: false,
        },
      },
      execute: wait_for_login,
    },
    check_login_status: {
      description: '检查指定平台或所有平台的登录状态',
      parameters: {
        platform: {
          type: 'string',
          description: '平台名称，不传则检查所有平台',
          required: false,
        },
      },
      execute: check_login_status,
    },
    logout_platform: {
      description: '退出指定平台的登录',
      parameters: {
        platform: {
          type: 'string',
          description: '平台名称',
          required: true,
        },
      },
      execute: logout_platform,
    },
    publish_article: {
      description: '发布文章到指定平台',
      parameters: {
        platform: {
          type: 'string',
          description: '平台名称',
          required: true,
        },
        title: {
          type: 'string',
          description: '文章标题',
          required: true,
        },
        content: {
          type: 'string',
          description: '文章内容',
          required: true,
        },
        coverImage: {
          type: 'string',
          description: '封面图片路径或URL',
          required: false,
        },
        tags: {
          type: 'array',
          description: '文章标签',
          required: false,
        },
        summary: {
          type: 'string',
          description: '文章摘要',
          required: false,
        },
        category: {
          type: 'string',
          description: '文章分类',
          required: false,
        },
        testMode: {
          type: 'boolean',
          description: '测试模式，为true时只填写文章不发布',
          required: false,
        },
      },
      execute: publish_article,
    },
    publish_to_all: {
      description: '发布文章到所有已登录的平台',
      parameters: {
        title: {
          type: 'string',
          description: '文章标题',
          required: true,
        },
        content: {
          type: 'string',
          description: '文章内容',
          required: true,
        },
        coverImage: {
          type: 'string',
          description: '封面图片路径或URL',
          required: false,
        },
        tags: {
          type: 'array',
          description: '文章标签',
          required: false,
        },
        summary: {
          type: 'string',
          description: '文章摘要',
          required: false,
        },
        category: {
          type: 'string',
          description: '文章分类',
          required: false,
        },
        testMode: {
          type: 'boolean',
          description: '测试模式，为true时只填写文章不发布',
          required: false,
        },
      },
      execute: publish_to_all,
    },
    list_platforms: {
      description: '列出所有支持的平台及其登录状态',
      parameters: {},
      execute: list_platforms,
    },
    get_category_options: {
      description: '获取指定平台支持的分类选项列表。OpenClaw应根据文章标题和内容，分析选择最合适的分类，然后调用publish_article时传入分类参数',
      parameters: {
        platform: {
          type: 'string',
          description: '平台名称，可选值: zhihu, bilibili, baijiahao, toutiao, xiaohongshu',
          required: true,
        },
      },
      execute: get_category_options,
    },
  },
};
