/**
 * 平台名称类型
 */
export type PlatformName = 'zhihu' | 'bilibili' | 'baijiahao' | 'toutiao' | 'xiaohongshu';

/**
 * 平台信息
 */
export interface PlatformInfo {
  name: PlatformName;
  displayName: string;
  loginUrl: string;
  publishUrl: string;
  domain: string;
}

/**
 * 文章内容
 */
export interface ArticleContent {
  title: string;
  content: string;
  coverImage?: string;
  tags?: string[];
  topic?: string;
  summary?: string;
  category?: string;
}

/**
 * 发布结果
 */
export interface PublishResult {
  success: boolean;
  platform: PlatformName;
  message: string;
  url?: string;
  error?: string;
  testMode?: boolean;
}

/**
 * 登录状态
 */
export interface LoginStatus {
  platform: PlatformName;
  isLoggedIn: boolean;
  lastLoginTime?: Date;
  expiresAt?: Date;
}

/**
 * Cookie数据
 */
export interface CookieData {
  cookies: Array<{
    name: string;
    value: string;
    domain: string;
    path: string;
    expires: number;
    httpOnly: boolean;
    secure: boolean;
    sameSite: 'Strict' | 'Lax' | 'None';
  }>;
  createdAt: string;
  expiresAt: string;
}

/**
 * 工具参数类型
 */
export interface LoginParams {
  platform: PlatformName;
}

export interface CheckLoginParams {
  platform?: PlatformName;
}

export interface LogoutParams {
  platform: PlatformName;
}

export interface PublishParams {
  platform: PlatformName;
  title: string;
  content: string;
  coverImage?: string;
  tags?: string[];
  summary?: string;
  category?: string;
  testMode?: boolean;
}

export interface PublishAllParams {
  title: string;
  content: string;
  coverImage?: string;
  tags?: string[];
  summary?: string;
  category?: string;
  testMode?: boolean;
}

export interface CoverImageInfo {
  id: number;
  photographer: string;
  url: string;
  preview: string;
  alt: string;
}

export interface GetCoverParams {
  title?: string;
  contentPreview?: string;
  keywords?: string;
  orientation?: 'landscape' | 'portrait' | 'square';
  size?: 'original' | 'large2x' | 'large' | 'medium' | 'small';
}

export interface GetCoverImagesParams extends GetCoverParams {
  count?: number;
}

/**
 * 工具执行结果
 */
export interface ToolResult {
  result: string;
  data?: unknown;
}

/**
 * 所有支持的平台信息
 */
export const PLATFORMS: Record<PlatformName, PlatformInfo> = {
  zhihu: {
    name: 'zhihu',
    displayName: '知乎',
    loginUrl: 'https://www.zhihu.com/signin',
    publishUrl: 'https://zhuanlan.zhihu.com/write',
    domain: 'zhihu.com',
  },
  bilibili: {
    name: 'bilibili',
    displayName: 'Bilibili',
    loginUrl: 'https://passport.bilibili.com/',
    publishUrl: 'https://member.bilibili.com/platform/upload/text/edit',
    domain: 'bilibili.com',
  },
  baijiahao: {
    name: 'baijiahao',
    displayName: '百家号',
    loginUrl: 'https://baijiahao.baidu.com/',
    publishUrl: 'https://baijiahao.baidu.com/builder/rc/edit',
    domain: 'baijiahao.baidu.com',
  },
  toutiao: {
    name: 'toutiao',
    displayName: '头条号',
    loginUrl: 'https://mp.toutiao.com/',
    publishUrl: 'https://mp.toutiao.com/publish',
    domain: 'toutiao.com',
  },
  xiaohongshu: {
    name: 'xiaohongshu',
    displayName: '小红书',
    loginUrl: 'https://www.xiaohongshu.com/',
    publishUrl: 'https://creator.xiaohongshu.com/publish/publish',
    domain: 'xiaohongshu.com',
  },
};
