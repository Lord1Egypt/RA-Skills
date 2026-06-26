export type DropType = 0 | 1;
export type DropEdition = "limited" | "open";
export type StageMode = 0 | 1;

export interface StageInput {
  stageID: number;
  stageName: string;
  price: string;
  duration: number;
  maxSupplyAtThisStage: number;
  maxMintedPerWallet: number;
  interval: number;
  stageMode: StageMode;
}

export interface CreateStageInput {
  stageID?: number;
  stageName: string;
  price: string;
  duration: number;
  maxSupplyAtThisStage: number;
  maxMintedPerWallet: number;
  interval: number;
  stageMode: StageMode;
}

export interface DropInput {
  chainMId: number;
  name: string;
  symbol: string;
  paymentToken?: string;
  preReveal: string;
  description: string;
  dropType: DropType;
  maxSupply: number;
  dropBeginTime: number;
  stages: StageInput[];
}

export interface CreateDropInput {
  chainMId: number;
  name: string;
  symbol: string;
  paymentToken?: string;
  preReveal?: string;
  previewMedia?: string[];
  description?: string;
  desc?: string;
  website?: string;
  twitter?: string;
  instagram?: string;
  discord?: string;
  telegram?: string;
  medium?: string;
  dropFeaturedImage?: string;
  edition?: DropEdition;
  dropType?: DropType;
  maxSupply?: number;
  dropBeginTime?: number;
  stages?: CreateStageInput[];
}

export interface CreateTokenRequest {
  chainMId: number;
  name: string;
  symbol: string;
}

export interface ElementBlockChainIdentity {
  chain: string;
  chainId: string;
}

export interface ElementIdentity {
  address: string;
  blockChain: ElementBlockChainIdentity;
}

export interface ElementChainCollectionSummary {
  id: string;
  slug: string;
}

export interface ElementCollectionContractResponse {
  chainCollection: ElementChainCollectionSummary | null;
}

export interface ElementCollectionSummary {
  id: string;
  name: string;
  slug: string;
}

export interface ElementUserCollectionListItem extends ElementCollectionSummary {
  imageUrl: string | null;
  featuredImageUrl: string | null;
  bannerImageUrl: string | null;
  isVerified: boolean;
  description: string | null;
  stats: {
    assetCount: number;
  };
  contracts: Array<{
    sourceType: string | null;
  }>;
}

export interface ElementCollectionContractInfo {
  blockChain: ElementBlockChainIdentity;
  address: string;
  sourceType: string | null;
}

export interface ElementCollectionDetailFromEditors {
  contracts: ElementCollectionContractInfo[];
  id: string;
  name: string;
  slug: string;
  description: string | null;
  imageUrl: string | null;
  bannerImageUrl: string | null;
  featuredImageUrl: string | null;
  externalUrl: string | null;
  weiboUrl: string | null;
  twitterUrl: string | null;
  instagramUrl: string | null;
  facebookUrl: string | null;
  mediumUrl: string | null;
  telegramUrl: string | null;
  discordUrl: string | null;
  categories: Array<{
    id: string;
    name: string;
    slug: string;
  }>;
  paymentTokens: Array<{
    id: string;
    name: string;
    address: string;
    symbol: string;
    chain: string;
    chainId: string;
  }>;
  royalty: number;
  royaltyAddress: string | null;
  isVerified: boolean;
}

export interface ElementLoginInput {
  identity: ElementIdentity;
  message: string;
  signature: string;
  realm?: string;
  source?: string;
}

export interface ElementCollectionEditInput {
  collectionId: string;
  token: string;
  imageFilePath?: string;
  name?: string;
  slug?: string;
  description?: string;
  image?: unknown;
  featuredImage?: unknown;
  bannerImage?: unknown;
  externalUrl?: string;
  weiboUrl?: string;
  twitterUrl?: string;
  instagramUrl?: string;
  facebookUrl?: string;
  mediumUrl?: string;
  telegramUrl?: string;
  discordUrl?: string;
  categories?: string[];
  paymentTokens?: string[];
  royalty?: number;
  royaltyAddress?: string;
}

export interface EncodedTransaction {
  from: string;
  to: string;
  value: string;
  data: string;
}

export interface ElementApiResponse<T> {
  code: number;
  message: string;
  data: T;
}

export interface OssSignSingleRequest {
  chainMId: number;
  contractAddress: string;
  mediaType: "prereveal" | "design";
}

export interface OssSignedPostData {
  accessid: string;
  policy: string;
  signature: string;
  dir: string;
  host: string;
  expire?: string;
  x_oss_credential?: string;
  x_oss_date?: string;
  security_token?: string;
  callback?: string;
}

export interface PreRevealUploadPayload {
  chainMId: number;
  contractAddress: string;
  dropType: DropType;
  preRevealExt: {
    image_url: string;
    animation_url: string;
  };
}

export interface DesignUploadPayload {
  dropID: number;
  chainMId?: number;
  contractAddress?: string;
  dropName: string;
  bannerURL: string;
  previewMediaExt: Array<{
    image_url: string;
    animation_url: string;
  }>;
  dropFeaturedImage: string;
  description: string;
  website: string;
  twitter: string;
  instagram: string;
  discord: string;
  telegram: string;
  medium: string;
  detailsUpdate: Array<{
    detailID?: number;
    template?: number;
    title?: string;
    description?: string;
    imageURL?: string;
    textAlign?: number | null;
    faq?: unknown;
  }>;
}

export interface CreateTokenPreflight {
  walletAddress: string;
  rpcUrl: string;
  authorization: string;
  nonce: string;
  loginMessage: string;
  identity: ElementIdentity;
}

export interface ExecutedTransactionReceipt {
  hash: string;
  blockNumber: number;
  status: number;
  gasUsed: string;
}

export interface ExecutedTransactionResult {
  hash: string;
  receipt: ExecutedTransactionReceipt;
  contractAddress?: string;
}

export interface GetDropSettingsQuery {
  chainMId: number;
  contractAddress: string;
}

export interface GetDropSettingsStage {
  stageID: number;
  stageName: string;
  price: string;
  interval: number;
  duration: number;
  maxSupplyAtThisStage: number;
  maxMintedPerWallet: number;
  stageMode: number;
  whiteListNum: number;
  enableCallFromContract: boolean;
  enableMintToOther: boolean;
  address?: string;
}

export interface PaymentTokenInfo {
  symbol?: string;
  address?: string;
  decimals?: number;
  chain?: string;
  chainId?: string;
  logoUrl?: string;
}

export interface GetDropSettingsResponse {
  dropID: number;
  published: number;
  maxSupply?: number;
  feeRecipient?: string;
  fee?: number;
  dropBeginTime?: number;
  isMinted: boolean;
  dropType: DropType;
  baseURI: string;
  isStageQuotaSharedForWallet: boolean;
  isPaused: boolean;
  mintingType: number;
  paymentToken?: PaymentTokenInfo;
  paymentTokens: PaymentTokenInfo[];
  mintFee: string;
  totalMint: number;
  batch: string;
  batchTime: number;
  stages: GetDropSettingsStage[];
}

export interface PostDropSettingsAllowList {
  address: string;
  buyCount: number;
}

export interface PostDropSettingsStageUpdate {
  stageID: number;
  stageName: string;
  price: string;
  interval: number;
  duration: number;
  maxMintedPerWallet: number;
  maxSupplyAtThisStage: number;
  stageMode: StageMode | null;
  allowListsNew: PostDropSettingsAllowList[];
}

export interface PostDropSettingsRequest {
  dropID: number;
  chainMId: number;
  contractAddress: string;
  dropType: DropType;
  maxSupply: number;
  fee: number;
  feeRecipient: string;
  mintingType: number;
  dropBeginTime: number;
  stagesUpdate: PostDropSettingsStageUpdate[];
}

export interface GetDropDesignQuery {
  dropID: number;
  chainMId: number;
  contractAddress: string;
}

export interface DropDesignDetail {
  detailID: number;
  template: number;
  title: string;
  description: string;
  imageURL: string;
  textAlign: number | null;
  faq: unknown;
}

export interface GetDropDesignResponse {
  dropID: number;
  dropName: string;
  bannerURL: string;
  previewMedia: string[];
  previewMediaExt: Array<{
    image_url?: string;
    animation_url?: string;
  }>;
  description: string;
  website: string;
  twitter: string;
  instagram: string;
  discord: string;
  telegram: string;
  medium: string;
  dropFeaturedImage: string;
  details: DropDesignDetail[];
}

export interface TempUrlMetaJson {
  [key: string]: unknown;
}

export interface GetTempURLQuery {
  chainMId: number;
  contractAddress: string;
  dropID: number;
  page: number;
  pageSize: number;
}

export interface GetTempURLResponse {
  preReveal: {
    image_url?: string;
    animation_url?: string;
    imageURL?: string;
    animationURL?: string;
  };
  metaPublish: boolean;
  metaDataIPFS: string;
  metaJsons: TempUrlMetaJson[];
  imgSum: number;
  metaSum: number;
  animationSum: number;
}

export interface GetPreRevealIPFSQuery {
  chainMId: number;
  contractAddress: string;
  dropID: number;
}

export interface GetPreRevealIPFSResponse {
  preRevealIPFS: string;
}

export interface CallbackUpdateProjectConfigRequest {
  dropId: number;
  chainMId: number;
  contractAddress: string;
}

export interface SetProjectConfigStageInput {
  stageID: number;
  stageName?: string;
  stageMode: number;
  price: string;
  address?: string;
  duration: number;
  maxSupplyAtThisStage: number;
  maxMintedPerWallet: number;
  interval: number;
  enableCallFromContract?: boolean;
  enableMintToOther?: boolean;
}

export interface SetProjectConfigRequest {
  chainMId: number;
  contractAddress: string;
  nftAddress: string;
  isPaused: boolean;
  dropBeginTime: number;
  maxSupply: string;
  baseURI: string;
  mintingType: number;
  stages: SetProjectConfigStageInput[];
}

export interface ChainListPaymentToken {
  ChainMId: number;
  SerId: number;
  TokenAddress: string;
  Enable: boolean;
  name: string;
  symbol?: string;
  icon: string;
  decimal: number;
  accuracy: number;
}

export interface ChainListWithGasItem {
  chainMId: number;
  currency: string;
  tokenCount: number;
  usdPrice: number;
  paymentTokens: ChainListPaymentToken[];
}

export interface GetChainsWithGasResponse {
  chains: ChainListWithGasItem[];
}
