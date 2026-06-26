import { ApiClient } from "./api-client";
export interface VideoMetadata {
    width: number;
    height: number;
    duration: number;
}
/**
 * 为远程视频 URL 提供默认元信息参数
 *
 * 服务端 submitTask 接口内部会通过 probeThreeTier 自动探测视频真实的 width/height/duration，
 * 并用探测到的真实值进行计费。这里返回一组安全的默认值作为 API 请求的 fallback 参数。
 */
export declare function probeVideoUrl(videoUrl: string, client: ApiClient): Promise<VideoMetadata>;
