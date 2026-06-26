import { buildDropUrls, createWorkflowLogger, runStage } from "./create-drop";
import type {
  ElementApiResponse,
  GetDropDesignResponse,
  GetDropSettingsResponse,
  GetTempURLResponse
} from "../types";

export interface PreviewDropFlowInput {
  authorization: string;
  walletAddress: string;
  chainMId: number;
  contractAddress: string;
  slug?: string;
  page?: number;
  pageSize?: number;
}

export interface PreviewDropFlowDeps {
  getDropSettings: (
    query: { chainMId: number; contractAddress: string },
    walletAddress: string
  ) => Promise<ElementApiResponse<GetDropSettingsResponse>>;
  getDropDesign: (
    query: { dropID: number; chainMId: number; contractAddress: string },
    walletAddress: string
  ) => Promise<ElementApiResponse<GetDropDesignResponse>>;
  getTempURL: (
    authorization: string,
    query: { chainMId: number; contractAddress: string; dropID: number; page: number; pageSize: number },
    walletAddress: string
  ) => Promise<ElementApiResponse<GetTempURLResponse>>;
}

function summarizePublishState(input: { published?: unknown; isPaused?: unknown }) {
  if (input.published !== 1) {
    return {
      status: "draft",
      label: "draft"
    };
  }
  if (input.isPaused === true) {
    return {
      status: "paused",
      label: "paused"
    };
  }
  return {
    status: "live",
    label: "live"
  };
}

export async function previewDropFlow(input: PreviewDropFlowInput, deps: PreviewDropFlowDeps) {
  const logger = createWorkflowLogger();
  const settings = await runStage(logger, "preview:getSettings", () =>
    deps.getDropSettings(
      {
        chainMId: input.chainMId,
        contractAddress: input.contractAddress
      },
      input.walletAddress
    )
  );

  const dropID = settings.data.dropID;
  const design =
    dropID > 0
      ? await runStage(logger, "preview:getDesign", () =>
        deps.getDropDesign(
          {
            dropID,
            chainMId: input.chainMId,
            contractAddress: input.contractAddress
          },
          input.walletAddress
        )
      )
      : null;
  const tempURL =
    dropID > 0
      ? await runStage(logger, "preview:getTempURL", () =>
        deps.getTempURL(
          input.authorization,
          {
            chainMId: input.chainMId,
            contractAddress: input.contractAddress,
            dropID,
            page: input.page ?? 1,
            pageSize: input.pageSize ?? 20
          },
          input.walletAddress
        )
      )
      : null;

  return {
    chainMId: input.chainMId,
    contractAddress: input.contractAddress,
    slug: input.slug ?? null,
    urls: input.slug ? buildDropUrls(input.slug) : null,
    settings,
    design,
    tempURL,
    summary: {
      slug: input.slug ?? null,
      ...(input.slug ? buildDropUrls(input.slug) : { dropUrl: null, collectionUrl: null, editUrl: null }),
      publishState: summarizePublishState({
        published: settings.data.published,
        isPaused: settings.data.isPaused
      }),
      batch: settings.data.batch,
      stageCount: settings.data.stages?.length ?? 0,
      hasDesign: Boolean(design?.data),
      hasPreRevealMedia: Boolean(
        tempURL?.data?.preReveal?.image_url?.trim() ?? tempURL?.data?.preReveal?.imageURL?.trim()
      )
    }
  };
}
