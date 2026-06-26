import { DEFAULT_DROP_API_BASE_URL } from "../config";
import { getJson, postJson } from "./http";
import type {
  CallbackUpdateProjectConfigRequest,
  CreateTokenRequest,
  GetDropDesignQuery,
  GetDropDesignResponse,
  GetPreRevealIPFSQuery,
  GetPreRevealIPFSResponse,
  GetDropSettingsQuery,
  GetDropSettingsResponse,
  DesignUploadPayload,
  ElementApiResponse,
  EncodedTransaction,
  GetChainsWithGasResponse,
  GetTempURLQuery,
  GetTempURLResponse,
  OssSignSingleRequest,
  OssSignedPostData,
  PostDropSettingsRequest,
  PreRevealUploadPayload,
  SetProjectConfigRequest
} from "../types";

export function createElementApiClient(baseUrl = DEFAULT_DROP_API_BASE_URL) {
  function withAuthHeaders(authorization: string, walletAddress?: string) {
    return {
      Authorization: authorization,
      ...(walletAddress ? { "x-viewer-addr": walletAddress } : {})
    };
  }

  function withOwnerHeaders(walletAddress?: string) {
    return walletAddress ? { "x-viewer-addr": walletAddress } : undefined;
  }

  return {
    async getChainsWithGas(): Promise<ElementApiResponse<GetChainsWithGasResponse>> {
      return getJson<ElementApiResponse<GetChainsWithGasResponse>>(`${baseUrl}/chain/listWithGas`);
    },

    async getDropSettings(
      query: GetDropSettingsQuery,
      walletAddress: string
    ): Promise<ElementApiResponse<GetDropSettingsResponse>> {
      const url = new URL(`${baseUrl}/edit/settings`);
      url.searchParams.set("chainMId", String(query.chainMId));
      url.searchParams.set("contractAddress", query.contractAddress);
      return getJson<ElementApiResponse<GetDropSettingsResponse>>(url.toString(), {
        headers: withOwnerHeaders(walletAddress)
      });
    },

    async postDropSettings(
      authorization: string,
      body: PostDropSettingsRequest,
      walletAddress: string
    ): Promise<ElementApiResponse<null>> {
      return postJson<ElementApiResponse<null>>(`${baseUrl}/edit/settings`, {
        body,
        headers: withAuthHeaders(authorization, walletAddress)
      });
    },

    async getDropDesign(
      query: GetDropDesignQuery,
      walletAddress: string
    ): Promise<ElementApiResponse<GetDropDesignResponse>> {
      const url = new URL(`${baseUrl}/edit/design`);
      url.searchParams.set("dropID", String(query.dropID));
      url.searchParams.set("chainMId", String(query.chainMId));
      url.searchParams.set("contractAddress", query.contractAddress);
      return getJson<ElementApiResponse<GetDropDesignResponse>>(url.toString(), {
        headers: withOwnerHeaders(walletAddress)
      });
    },

    async postCreateToken(
      authorization: string,
      body: CreateTokenRequest,
      walletAddress?: string
    ): Promise<ElementApiResponse<EncodedTransaction>> {
      return postJson<ElementApiResponse<EncodedTransaction>>(`${baseUrl}/encode/createToken`, {
        body,
        headers: withAuthHeaders(authorization, walletAddress)
      });
    },

    async getOssSignSingle(
      authorization: string,
      query: OssSignSingleRequest,
      walletAddress?: string
    ): Promise<ElementApiResponse<OssSignedPostData>> {
      const url = new URL(`${baseUrl}/oss/signSingle`);
      url.searchParams.set("chainMId", String(query.chainMId));
      url.searchParams.set("contractAddress", query.contractAddress);
      url.searchParams.set("mediaType", query.mediaType);
      return getJson<ElementApiResponse<OssSignedPostData>>(url.toString(), {
        headers: withAuthHeaders(authorization, walletAddress)
      });
    },

    async postPreReveal(
      authorization: string,
      body: PreRevealUploadPayload,
      walletAddress?: string
    ): Promise<ElementApiResponse<null>> {
      return postJson<ElementApiResponse<null>>(`${baseUrl}/edit/upload/preReveal`, {
        body,
        headers: withAuthHeaders(authorization, walletAddress)
      });
    },

    async postDesign(
      authorization: string,
      body: DesignUploadPayload,
      walletAddress?: string
    ): Promise<ElementApiResponse<null>> {
      return postJson<ElementApiResponse<null>>(`${baseUrl}/edit/design`, {
        body,
        headers: withAuthHeaders(authorization, walletAddress)
      });
    },

    async getPreRevealIPFS(
      query: GetPreRevealIPFSQuery,
      walletAddress: string
    ): Promise<ElementApiResponse<GetPreRevealIPFSResponse>> {
      const url = new URL(`${baseUrl}/edit/upload/preRevealIPFS`);
      url.searchParams.set("chainMId", String(query.chainMId));
      url.searchParams.set("contractAddress", query.contractAddress);
      url.searchParams.set("dropID", String(query.dropID));
      return getJson<ElementApiResponse<GetPreRevealIPFSResponse>>(url.toString(), {
        headers: withOwnerHeaders(walletAddress)
      });
    },

    async getTempURL(
      authorization: string,
      query: GetTempURLQuery,
      walletAddress: string
    ): Promise<ElementApiResponse<GetTempURLResponse>> {
      const url = new URL(`${baseUrl}/edit/upload/tempURL`);
      url.searchParams.set("chainMId", String(query.chainMId));
      url.searchParams.set("contractAddress", query.contractAddress);
      url.searchParams.set("dropID", String(query.dropID));
      url.searchParams.set("page", String(query.page));
      url.searchParams.set("pageSize", String(query.pageSize));
      return getJson<ElementApiResponse<GetTempURLResponse>>(url.toString(), {
        headers: withAuthHeaders(authorization, walletAddress)
      });
    },

    async postSetProjectConfig(
      authorization: string,
      body: SetProjectConfigRequest,
      walletAddress: string
    ): Promise<ElementApiResponse<EncodedTransaction>> {
      return postJson<ElementApiResponse<EncodedTransaction>>(`${baseUrl}/encode/setProjectConfig`, {
        body,
        headers: withAuthHeaders(authorization, walletAddress)
      });
    },

    async postCallbackUpdateProjectConfig(
      body: CallbackUpdateProjectConfigRequest
    ): Promise<ElementApiResponse<null>> {
      return postJson<ElementApiResponse<null>>(`${baseUrl}/callback/updateProjectConfig`, {
        body
      });
    }
  };
}
