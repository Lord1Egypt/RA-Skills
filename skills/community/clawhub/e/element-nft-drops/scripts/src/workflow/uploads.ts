import { createCuimpHttp } from "cuimp";
import type { CuimpInstance } from "cuimp";
import { DEFAULT_OSS_UPLOAD_TIMEOUT_MS } from "../config";
import {
  assertSafeUploadFileName,
  inferUploadExtension,
  validateLocalImageUpload
} from "../security/upload-guard";
import type {
  DesignUploadPayload,
  DropType,
  ElementApiResponse,
  OssSignedPostData,
  PreRevealUploadPayload
} from "../types";

export interface UploadedAssetRef {
  sourcePath: string;
  fileName: string;
  objectKey: string;
  publicUrl: string;
}

export interface UploadAuthContext {
  authorization: string;
  walletAddress: string;
}

export interface PreRevealUploadInput {
  mode: "prereveal";
  chainMId: number;
  contractAddress: string;
  dropType: DropType;
  filePath: string;
}

export interface DesignUploadInput {
  mode: "design";
  chainMId: number;
  contractAddress: string;
  dropID: number;
  dropName: string;
  bannerFilePath?: string;
  previewFilePaths: string[];
}

export type UploadInput = PreRevealUploadInput | DesignUploadInput;

export interface UploadDeps {
  getOssSignSingle: (
    authorization: string,
    query: { chainMId: number; contractAddress: string; mediaType: "prereveal" | "design" },
    walletAddress?: string
  ) => Promise<ElementApiResponse<OssSignedPostData>>;
  postPreReveal: (
    authorization: string,
    body: PreRevealUploadPayload,
    walletAddress?: string
  ) => Promise<ElementApiResponse<null>>;
  uploadAsset: (input: {
    filePath: string;
    fileName: string;
    oss: OssSignedPostData;
  }) => Promise<UploadedAssetRef>;
}

export interface CuimpUploadDeps {
  createClient?: () => Pick<CuimpInstance, "request">;
}

function withTimeout<T>(promise: Promise<T>, ms: number, label: string): Promise<T> {
  return new Promise<T>((resolve, reject) => {
    const timeoutHandle = setTimeout(() => {
      reject(new Error(`${label} timed out after ${ms}ms`));
    }, ms);

    promise.then(
      (value) => {
        clearTimeout(timeoutHandle);
        resolve(value);
      },
      (error) => {
        clearTimeout(timeoutHandle);
        reject(error);
      }
    );
  });
}

export function convertOssUrlToPublicUrl(url: string): string {
  return url
    .replace(
      "https://element-master.oss-cn-hongkong.aliyuncs.com/creator-studio/",
      "https://c.nfte.ai/creator-studio/"
    )
    .replace("https://ele-lpd.nfte.ai/", "https://c.nfte.ai/");
}

export function buildPreRevealUploadPayload(input: {
  chainMId: number;
  contractAddress: string;
  dropType: DropType;
  publicUrl: string;
}): PreRevealUploadPayload {
  return {
    chainMId: input.chainMId,
    contractAddress: input.contractAddress,
    dropType: input.dropType,
    preRevealExt: {
      image_url: input.publicUrl,
      animation_url: ""
    }
  };
}

export function buildDesignUploadPayload(input: {
  chainMId: number;
  contractAddress: string;
  dropID: number;
  dropName: string;
  bannerUrl?: string;
  previewUrls: string[];
}): DesignUploadPayload {
  return {
    dropID: input.dropID,
    chainMId: input.chainMId,
    contractAddress: input.contractAddress,
    dropName: input.dropName,
    bannerURL: input.bannerUrl ?? "",
    previewMediaExt: input.previewUrls.map((url) => ({
      image_url: url,
      animation_url: ""
    })),
    dropFeaturedImage: "",
    description: "",
    website: "",
    twitter: "",
    instagram: "",
    discord: "",
    telegram: "",
    medium: "",
    detailsUpdate: []
  };
}

export async function uploadAssetGroupWithExistingAuthorization(input: {
  auth: UploadAuthContext;
  chainMId: number;
  contractAddress: string;
  mediaType: "prereveal" | "design";
  files: Array<{
    filePath: string;
    fileName: string;
  }>;
}, deps: Pick<UploadDeps, "getOssSignSingle" | "uploadAsset">): Promise<UploadedAssetRef[]> {
  const uploads: UploadedAssetRef[] = [];

  for (const file of input.files) {
    const sign = await deps.getOssSignSingle(
      input.auth.authorization,
      {
        chainMId: input.chainMId,
        contractAddress: input.contractAddress,
        mediaType: input.mediaType
      },
      input.auth.walletAddress
    );
    uploads.push(
      await deps.uploadAsset({
        filePath: file.filePath,
        fileName: file.fileName,
        oss: sign.data
      })
    );
  }

  return uploads;
}

export async function uploadSingleAsset(input: {
  filePath: string;
  fileName: string;
  oss: OssSignedPostData;
}, deps: CuimpUploadDeps = {}): Promise<UploadedAssetRef> {
  return uploadAssetWithCuimp(input, deps);
}

export async function uploadAssetWithCuimp(
  input: {
    filePath: string;
    fileName: string;
    oss: OssSignedPostData;
  },
  deps: CuimpUploadDeps = {}
): Promise<UploadedAssetRef> {
  assertSafeUploadFileName(input.fileName);
  const validated = await validateLocalImageUpload(input.filePath);
  const objectKey = `${input.oss.dir.replace(/\/$/, "")}/${input.fileName}`;
  const mimeType = validated.mimeType;
  const extraCurlArgs = [
    "-F",
    `name=${input.fileName}`,
    "-F",
    `key=${objectKey}`,
    "-F",
    "success_action_status=200",
    "-F",
    `policy=${input.oss.policy}`
  ];

  if (input.oss.x_oss_credential && input.oss.x_oss_date) {
    extraCurlArgs.push("-F", `x-oss-signature=${input.oss.signature}`);
    extraCurlArgs.push("-F", "x-oss-signature-version=OSS4-HMAC-SHA256");
    extraCurlArgs.push("-F", `x-oss-credential=${input.oss.x_oss_credential}`);
    extraCurlArgs.push("-F", `x-oss-date=${input.oss.x_oss_date}`);
    if (input.oss.security_token) {
      extraCurlArgs.push("-F", `x-oss-security-token=${input.oss.security_token}`);
    }
    if (input.oss.callback) {
      extraCurlArgs.push("-F", `callback=${input.oss.callback}`);
    }
  } else {
    extraCurlArgs.push("-F", `OSSAccessKeyId=${input.oss.accessid}`);
    extraCurlArgs.push("-F", `signature=${input.oss.signature}`);
  }

  extraCurlArgs.push(
    "-F",
    `file=@${validated.realPath};type=${mimeType};filename=${input.fileName}`
  );

  const client =
    (deps.createClient ??
      (() => createCuimpHttp()))();
  const response = await withTimeout(
    client.request({
      url: input.oss.host,
      method: "POST",
      headers: {
        Accept: "*/*",
        Referer: "https://element.market/",
        Origin: "https://element.market"
      },
      extraCurlArgs
    }),
    DEFAULT_OSS_UPLOAD_TIMEOUT_MS,
    `OSS upload request to ${input.oss.host}`
  );
  const responseRecord = response as unknown as Record<string, unknown>;
  const responseBody =
    "data" in responseRecord
      ? responseRecord.data
      : "body" in responseRecord
        ? responseRecord.body
        : response;

  if (response.status !== 200) {
    console.error(
      `[element-drop] external response ${JSON.stringify({
        method: "POST",
        url: input.oss.host,
        status: response.status,
        body: responseBody
      })}`
    );
    throw new Error(
      `OSS upload failed with status ${response.status}: ${typeof responseBody === "string" ? responseBody : JSON.stringify(responseBody)}`
    );
  }

  const publicUrl = convertOssUrlToPublicUrl(`${input.oss.host}/${objectKey}`);
  return {
    sourcePath: validated.realPath,
    fileName: input.fileName,
    objectKey,
    publicUrl
  };
}

function inferExtension(filePath: string): string {
  return inferUploadExtension(filePath);
}

export async function uploadWithExistingAuthorization(
  auth: UploadAuthContext,
  input: UploadInput,
  deps: UploadDeps
) {
  if (input.mode === "prereveal") {
    const [asset] = await uploadAssetGroupWithExistingAuthorization(
      {
        auth,
        chainMId: input.chainMId,
        contractAddress: input.contractAddress,
        mediaType: "prereveal",
        files: [
          {
            filePath: input.filePath,
            fileName: `pre-reveal${inferExtension(input.filePath)}`
          }
        ]
      },
      deps
    );

    const payload = buildPreRevealUploadPayload({
      chainMId: input.chainMId,
      contractAddress: input.contractAddress,
      dropType: input.dropType,
      publicUrl: asset.publicUrl
    });
    const response = await deps.postPreReveal(auth.authorization, payload, auth.walletAddress);
    return {
      mode: "prereveal" as const,
      uploads: [asset],
      publicUrls: [asset.publicUrl],
      payload,
      response
    };
  }

  const uploads = await uploadAssetGroupWithExistingAuthorization(
    {
      auth,
      chainMId: input.chainMId,
      contractAddress: input.contractAddress,
      mediaType: "design",
      files: [
        ...(input.bannerFilePath
          ? [
              {
                filePath: input.bannerFilePath,
                fileName: `banner${inferExtension(input.bannerFilePath)}`
              }
            ]
          : []),
        ...input.previewFilePaths.map((filePath, index) => ({
          filePath,
          fileName: `preview-${index + 1}${inferExtension(filePath)}`
        }))
      ]
    },
    deps
  );
  const bannerUpload = input.bannerFilePath ? uploads[0] : null;
  const previewUploads = input.bannerFilePath ? uploads.slice(1) : uploads;

  const payload = buildDesignUploadPayload({
    chainMId: input.chainMId,
    contractAddress: input.contractAddress,
    dropID: input.dropID,
    dropName: input.dropName,
    bannerUrl: bannerUpload?.publicUrl,
    previewUrls: previewUploads.map((item) => item.publicUrl)
  });
  return {
    mode: "design" as const,
    uploads,
    publicUrls: uploads.map((item) => item.publicUrl),
    payload
  };
}
