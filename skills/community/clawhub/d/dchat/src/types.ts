/** Content types compatible with dchat/nMobile protocol */
export type MessageContentType =
  | "text"
  | "textExtension"
  | "image"
  | "audio"
  | "file"
  | "receipt"
  | "read"
  | "contact"
  | "contactOptions";

export type MessageStatus = "sending" | "sent" | "delivered" | "read" | "failed";

/** Wire format: JSON sent over NKN between peers */
export interface MessageData {
  id: string;
  contentType: MessageContentType;
  content?: string;
  options?: MessageOptions;
  topic?: string;
  targetID?: string; // for receipts: original message ID
  readIds?: string[]; // for read receipts
  timestamp: number;
}

/** nMobile-compatible message options for media/encryption metadata */
export interface MessageOptions {
  deleteAfterSeconds?: number;
  updateBurnAfterAt?: number;

  // IPFS media (nMobile format)
  ipfsHash?: string;
  ipfsIp?: string;
  ipfsEncrypt?: number; // 1 = encrypted
  ipfsEncryptAlgorithm?: string; // "AES/GCM/NoPadding"
  ipfsEncryptKeyBytes?: number[]; // AES key as byte array
  ipfsEncryptNonceSize?: number; // 12

  // Thumbnail (images only)
  ipfsThumbnailHash?: string;
  ipfsThumbnailIp?: string;
  ipfsThumbnailEncrypt?: number;
  ipfsThumbnailEncryptAlgorithm?: string;
  ipfsThumbnailEncryptKeyBytes?: number[];
  ipfsThumbnailEncryptNonceSize?: number;

  // File metadata
  fileType?: number; // 0=file, 1=image, 2=audio
  fileName?: string;
  fileExt?: string;
  fileMimeType?: string;
  fileSize?: number;
  mediaWidth?: number;
  mediaHeight?: number;
  mediaDuration?: number; // seconds
}

/** Stored message record */
export interface Message {
  id: string;
  sender: string;
  receiver: string;
  contentType: MessageContentType;
  content: string;
  status: MessageStatus;
  isOutbound: boolean;
  options?: string; // JSON-serialized MessageOptions
  localFilePath?: string;
  deleteAt?: number;
  createdAt: number;
}

/** NKN client connection state */
export interface ClientStatus {
  state: "disconnected" | "connecting" | "connected";
  address?: string;
  publicKey?: string;
}

/** Incoming message event payload */
export interface IncomingMessage {
  id: string;
  from: string;
  contentType: MessageContentType;
  content: string;
  options?: MessageOptions;
  timestamp: number;
  /** Local path to downloaded media file (populated after auto-download) */
  localFilePath?: string;
}

/** IPFS gateway configuration */
export interface IpfsGateway {
  host: string;
  port: number;
  protocol: "http:" | "https:";
  authHeader?: string;
}

/** Bot configuration */
export interface BotConfig {
  /** NKN wallet seed (hex string). Generated if not provided. */
  seed?: string;
  /** Data directory for cache and database. Defaults to ~/.dchat-clawhub */
  dataDir?: string;
  /** IPFS gateways. Defaults to nMobile gateway. */
  ipfsGateways?: IpfsGateway[];
  /** Number of NKN sub-clients. Default: 4 */
  numSubClients?: number;
  /** Auto-download received media files. Default: true */
  autoDownloadMedia?: boolean;
}
