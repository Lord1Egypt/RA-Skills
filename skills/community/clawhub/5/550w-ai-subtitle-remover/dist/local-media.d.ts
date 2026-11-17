import * as fs from "fs";
type LocalMediaKind = "video" | "image";
export declare function openSelectedLocalMedia(filePath: string, kind: LocalMediaKind): {
    name: string;
    size: number;
    data: fs.ReadStream;
};
export {};
