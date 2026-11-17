export interface VideoMetadata {
    width: number;
    height: number;
    duration: number;
}
export declare function assertPublicVideoUrl(videoUrl: string): Promise<void>;
/**
 * 使用本机 ffprobe 获取远程视频的真实元信息。不得伪造默认宽高和时长：这些字段既参与
 * 服务端快速拒绝，也可能在远程媒体暂时无法探测时成为兜底依据。
 */
export declare function probeVideoUrl(videoUrl: string): Promise<VideoMetadata>;
