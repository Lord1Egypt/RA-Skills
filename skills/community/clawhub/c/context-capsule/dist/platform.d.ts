/** SHA-256 of a UTF-8 string (or raw bytes) -> 32 bytes. */
export declare function sha256Bytes(data: string | Uint8Array): Uint8Array;
/** SHA-256 of a UTF-8 string -> lowercase hex. */
export declare function sha256Hex(data: string): string;
/** SHA-256 of (a ‖ b) raw bytes — the merkle internal-node hash. */
export declare function sha256Concat(a: Uint8Array, b: Uint8Array): Uint8Array;
/** Deflate (zlib, level 9) a UTF-8 string -> base64 + raw byte length. */
export declare function deflate(text: string): {
    base64: string;
    bytes: number;
};
export declare function utf8ByteLength(text: string): number;
export declare function zeroBytes(n: number): Uint8Array;
export declare function bytesToHex(bytes: Uint8Array): string;
