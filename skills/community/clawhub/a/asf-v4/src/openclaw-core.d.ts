/**
 * OpenClaw Core 类型声明
 */

declare module '@openclaw/core' {
  export function video_generate(params: {
    action?: 'generate' | 'status' | 'list';
    prompt?: string;
    image?: string;
    images?: string[];
    video?: string;
    videos?: string[];
    durationSeconds?: number;
    resolution?: '480P' | '720P' | '1080P';
    aspectRatio?: string;
    size?: string;
    model?: string;
    audio?: boolean;
    watermark?: boolean;
    filename?: string;
  }): Promise<any>;
}
