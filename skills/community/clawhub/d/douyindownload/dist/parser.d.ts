export interface ParseResult {
    success: boolean;
    title?: string;
    author?: string;
    coverUrl?: string;
    videoUrl?: string;
    platform: 'douyin' | 'unknown';
    videoId?: string;
    error?: string;
}
export declare function parseVideo(url: string): Promise<ParseResult>;
//# sourceMappingURL=parser.d.ts.map