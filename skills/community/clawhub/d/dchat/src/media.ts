import fs from "fs";
import path from "path";
import { encrypt, decrypt } from "./crypto.js";
import { IpfsService } from "./ipfs.js";
import type { MessageOptions } from "./types.js";

const MAX_FILE_SIZE = 100 * 1024 * 1024; // 100 MB

export interface MediaResult {
  content: string; // IPFS hash or inline base64
  options: MessageOptions;
  localFilePath: string;
}

export class MediaService {
  private cacheDir: string;
  private ipfs: IpfsService;

  constructor(ipfs: IpfsService, dataDir: string) {
    this.ipfs = ipfs;
    this.cacheDir = path.join(dataDir, "media-cache");
    fs.mkdirSync(this.cacheDir, { recursive: true });
  }

  /**
   * Process and upload an image file.
   * Bot-optimized: no thumbnail generation (no sharp dependency), sends full image only.
   * Still nMobile-compatible wire format.
   */
  async uploadImage(filePath: string): Promise<MediaResult> {
    const imageBuffer = fs.readFileSync(filePath);
    if (imageBuffer.length > MAX_FILE_SIZE) {
      throw new Error(`File too large: ${imageBuffer.length} bytes (max ${MAX_FILE_SIZE})`);
    }

    const ext = path.extname(filePath).replace(/^\./, "") || "jpg";
    const { ciphertext, key } = encrypt(imageBuffer);
    const ipfsHash = await this.ipfs.upload(ciphertext, "image.enc");
    const primaryIp = this.ipfs.getPrimaryIp();

    const localFilePath = path.join(this.cacheDir, `${ipfsHash}.${ext}`);
    fs.writeFileSync(localFilePath, imageBuffer);

    const options: MessageOptions = {
      ipfsHash,
      ipfsIp: primaryIp,
      ipfsEncrypt: 1,
      ipfsEncryptAlgorithm: "AES/GCM/NoPadding",
      ipfsEncryptKeyBytes: Array.from(key),
      ipfsEncryptNonceSize: 12,
      fileType: 1,
      fileExt: ext,
      fileMimeType: `image/${ext === "jpg" ? "jpeg" : ext}`,
      fileSize: imageBuffer.length,
    };

    return { content: ipfsHash, options, localFilePath };
  }

  /**
   * Process and upload an audio file.
   * Sends as inline base64 in nMobile data-URI format for small files,
   * or via IPFS for larger ones.
   */
  async uploadAudio(filePath: string, durationSeconds?: number): Promise<MediaResult> {
    const audioBuffer = fs.readFileSync(filePath);
    if (audioBuffer.length > MAX_FILE_SIZE) {
      throw new Error(`File too large: ${audioBuffer.length} bytes (max ${MAX_FILE_SIZE})`);
    }

    const ext = path.extname(filePath).replace(/^\./, "") || "aac";
    const localFilePath = path.join(this.cacheDir, `${Date.now()}.${ext}`);
    fs.writeFileSync(localFilePath, audioBuffer);

    const options: MessageOptions = {
      fileType: 2,
      fileExt: ext,
      fileMimeType: `audio/${ext}`,
      mediaDuration: durationSeconds,
    };

    // Inline for small audio (<256KB), IPFS for larger
    if (audioBuffer.length < 256 * 1024) {
      const content = `![audio](data:audio/x-${ext};base64,${audioBuffer.toString("base64")})`;
      return { content, options, localFilePath };
    }

    // Large audio: encrypt and upload to IPFS
    const { ciphertext, key } = encrypt(audioBuffer);
    const ipfsHash = await this.ipfs.upload(ciphertext, `audio.${ext}.enc`);
    options.ipfsHash = ipfsHash;
    options.ipfsIp = this.ipfs.getPrimaryIp();
    options.ipfsEncrypt = 1;
    options.ipfsEncryptAlgorithm = "AES/GCM/NoPadding";
    options.ipfsEncryptKeyBytes = Array.from(key);
    options.ipfsEncryptNonceSize = 12;
    options.fileSize = audioBuffer.length;

    return { content: ipfsHash, options, localFilePath };
  }

  /**
   * Process and upload a generic file.
   */
  async uploadFile(filePath: string): Promise<MediaResult> {
    const fileBuffer = fs.readFileSync(filePath);
    if (fileBuffer.length > MAX_FILE_SIZE) {
      throw new Error(`File too large: ${fileBuffer.length} bytes (max ${MAX_FILE_SIZE})`);
    }

    const fileName = path.basename(filePath);
    const ext = path.extname(filePath).replace(/^\./, "") || "bin";
    const { ciphertext, key } = encrypt(fileBuffer);
    const ipfsHash = await this.ipfs.upload(ciphertext, `${fileName}.enc`);
    const primaryIp = this.ipfs.getPrimaryIp();

    const localFilePath = path.join(this.cacheDir, `${ipfsHash}.${ext}`);
    fs.writeFileSync(localFilePath, fileBuffer);

    const options: MessageOptions = {
      fileType: 0,
      fileName,
      fileExt: ext,
      fileSize: fileBuffer.length,
      ipfsHash,
      ipfsIp: primaryIp,
      ipfsEncrypt: 1,
      ipfsEncryptAlgorithm: "AES/GCM/NoPadding",
      ipfsEncryptKeyBytes: Array.from(key),
      ipfsEncryptNonceSize: 12,
    };

    return { content: ipfsHash, options, localFilePath };
  }

  /**
   * Download and decrypt media from IPFS.
   * Returns local file path.
   */
  async downloadMedia(
    ipfsHash: string,
    keyBytes: number[],
    nonceSize = 12,
    fileExt = "bin",
    preferredIp?: string,
  ): Promise<string> {
    const ext = fileExt.startsWith(".") ? fileExt : `.${fileExt}`;
    const cachedPath = path.join(this.cacheDir, `${ipfsHash}${ext}`);
    if (fs.existsSync(cachedPath)) return cachedPath;

    const encryptedData = await this.ipfs.download(ipfsHash, preferredIp);
    const key = Buffer.from(keyBytes);
    const decrypted = decrypt(encryptedData, key, nonceSize);
    fs.writeFileSync(cachedPath, decrypted);
    return cachedPath;
  }

  /**
   * Save inline audio (nMobile base64 data-URI format) to local cache.
   */
  saveInlineAudio(messageId: string, content: string, fileExt = "aac"): string {
    const ext = fileExt.startsWith(".") ? fileExt : `.${fileExt}`;
    const localPath = path.join(this.cacheDir, `${messageId}${ext}`);
    const match = content.match(/^!\[audio\]\(data:[^;]+;base64,(.+)\)$/s);
    const rawBase64 = match ? match[1] : content;
    fs.writeFileSync(localPath, Buffer.from(rawBase64, "base64"));
    return localPath;
  }

  getCacheDir(): string {
    return this.cacheDir;
  }
}
