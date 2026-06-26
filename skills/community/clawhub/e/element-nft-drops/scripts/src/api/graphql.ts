import { createHmac, randomInt } from "node:crypto";
import {
  DEFAULT_ELEMENT_GRAPHQL_URL,
  DEFAULT_NETWORK_TIMEOUT_MS,
  resolveElementGraphqlTokenA,
  resolveElementGraphqlTokenB
} from "../config";
import { readValidatedLocalImageUpload } from "../security/upload-guard";
import { postJson } from "./http";
import type {
  ElementCollectionContractResponse,
  ElementCollectionDetailFromEditors,
  ElementCollectionEditInput,
  ElementCollectionSummary,
  ElementIdentity,
  ElementLoginInput,
  ElementUserCollectionListItem
} from "../types";

export const ELEMENT_LOGIN_NONCE_QUERY = `
    query GetNonce($address: Address!, $chain: Chain!, $chainId: ChainId!) {
        user(identity: { address: $address, blockChain: { chain: $chain, chainId: $chainId } }) {
            nonce
        }
    }
`;

export const ELEMENT_LOGIN_AUTH_MUTATION = `
    mutation LoginAuth($identity: IdentityInput!, $message: String!, $signature: String!, $realm: String, $source: String) {
        auth {
            login(input: { identity: $identity, message: $message, signature: $signature, realm: $realm, source: $source }) {
                token
            }
        }
    }
`;

export const COLLECTION_CONTRACT_QUERY = `query CollectionContract($address: Address!, $blockChain: BlockChainInput!) {
  contract(identity: { address: $address, blockChain: $blockChain }) {
    chainCollection {
      id
      slug
    }
  }
}
`;

export const GET_MUTATE_TOKEN_QUERY = `query GetMutateToken {
  mutateToken {
    token
  }
}
`;

export const COLLECTION_DETAIL_FROM_EDITORS_QUERY = `query CollectionDetailFromEditors($slug: String!) {
  collection(slug: $slug) {
    contracts {
      blockChain {
        chain
        chainId
      }
      address
      sourceType
    }
    id
    name
    slug
    description
    imageUrl
    bannerImageUrl
    featuredImageUrl
    externalUrl
    weiboUrl
    twitterUrl
    instagramUrl
    facebookUrl
    mediumUrl
    telegramUrl
    discordUrl
    categories {
      id
      name
      nameCN
      nameKR
      slug
      imageUrl
      description
    }
    paymentTokens {
      id
      name
      address
      icon
      symbol
      chain
      chainId
    }
    royalty
    royaltyAddress
    isVerified
    owners {
      identity {
        address
        blockChain {
          chain
          chainId
        }
      }
      user {
        id
        address
        profileImageUrl
        userName
        bio
      }
      info {
        profileImageUrl
        userName
      }
    }
    editors {
      identity {
        address
        blockChain {
          chain
          chainId
        }
      }
    }
    stats {
      assetCount
    }
  }
}
`;

export const COLLECTION_EDIT_MUTATION = `mutation collectionEdit($collectionId: ID!, $name: String, $slug: String, $description: String, $image: Upload, $featuredImage: Upload, $bannerImage: Upload, $externalUrl: String, $weiboUrl: String, $twitterUrl: String, $instagramUrl: String, $facebookUrl: String, $mediumUrl: String, $telegramUrl: String, $discordUrl: String, $categories: [String!], $paymentTokens: [String!], $royalty: Int, $royaltyAddress: Address, $token: String!) {
  collections {
    modify(
      input: {collectionId: $collectionId, name: $name, slug: $slug, description: $description, image: $image, featuredImage: $featuredImage, bannerImage: $bannerImage, externalUrl: $externalUrl, weiboUrl: $weiboUrl, twitterUrl: $twitterUrl, instagramUrl: $instagramUrl, facebookUrl: $facebookUrl, mediumUrl: $mediumUrl, telegramUrl: $telegramUrl, discordUrl: $discordUrl, categories: $categories, paymentTokens: $paymentTokens, royalty: $royalty, royaltyAddress: $royaltyAddress}
      mutateToken: {token: $token}
    ) {
      id
      name
      slug
    }
  }
}
`;

export const USER_COLLECTION_LIST_QUERY = `query UserCollectionList($before: String, $after: String, $first: Int, $last: Int, $owners: [IdentityInput!], $editors: [IdentityInput!], $blockChains: [BlockChainInput!]) {
  collectionSearch(
    before: $before
    after: $after
    first: $first
    last: $last
    input: {owners: $owners, editors: $editors, blockChains: $blockChains}
  ) {
    edges {
      cursor
      node {
        id
        name
        slug
        imageUrl
        featuredImageUrl
        bannerImageUrl
        isVerified
        description
        stats {
          assetCount
        }
        contracts {
          sourceType
        }
      }
    }
    pageInfo {
      startCursor
      endCursor
      hasPreviousPage
      hasNextPage
    }
  }
}
`;

interface LoginNonceResponse {
  errors?: Array<{
    message?: string;
  }>;
  data?: {
    user?: {
      nonce?: number | string | null;
    } | null;
  };
}

interface LoginAuthResponse {
  errors?: Array<{
    message?: string;
  }>;
  data?: {
    auth?: {
      login?: {
        token?: string | null;
      } | null;
    } | null;
  };
}

interface CollectionContractResponse {
  errors?: Array<{
    message?: string;
  }>;
  data?: {
    contract?: ElementCollectionContractResponse | null;
  };
}

interface GetMutateTokenResponse {
  errors?: Array<{
    message?: string;
  }>;
  data?: {
    mutateToken?: {
      token?: string | null;
    } | null;
  };
}

interface CollectionDetailFromEditorsResponse {
  errors?: Array<{
    message?: string;
  }>;
  data?: {
    collection?: ElementCollectionDetailFromEditors | null;
  };
}

interface CollectionEditResponse {
  errors?: Array<{
    message?: string;
  }>;
  data?: {
    collections?: {
      modify?: ElementCollectionSummary | null;
    } | null;
  };
}

interface UserCollectionListResponse {
  errors?: Array<{
    message?: string;
  }>;
  data?: {
    collectionSearch?: {
      edges?: Array<{
        cursor: string;
        node: ElementUserCollectionListItem;
      }>;
      pageInfo?: {
        startCursor?: string | null;
        endCursor?: string | null;
        hasPreviousPage?: boolean;
        hasNextPage?: boolean;
      };
    } | null;
  };
}

export function buildElementGraphqlGatewayHeaders(input?: {
  tokenA?: string;
  tokenB?: string;
  nonce?: number;
  timestamp?: number;
}): Record<string, string> {
  const tokenA = input?.tokenA ?? resolveElementGraphqlTokenA();
  const tokenB = input?.tokenB ?? resolveElementGraphqlTokenB();
  const nonce = String(input?.nonce ?? randomInt(1000, 10000));
  const timestamp = String(input?.timestamp ?? Math.floor(Date.now() / 1000));
  const signature = createHmac("sha256", tokenB)
    .update(`${tokenA}${nonce}${timestamp}`)
    .digest("hex");

  return {
    "x-api-key": tokenA,
    "x-api-sign": `${signature}.${nonce}.${timestamp}`,
    origin: "https://element.market",
    referer: "https://element.market/",
    "user-agent": "Mozilla/5.0"
  };
}

function withOptionalAuthorization(
  headers: Record<string, string>,
  authorization?: string
): Record<string, string> {
  return authorization ? { ...headers, Authorization: authorization } : headers;
}

async function postGraphqlMultipart<T>(input: {
  url: string;
  operationName: string;
  variables: Record<string, unknown>;
  query: string;
  fileFieldMap: Record<string, string[]>;
  fileParts: Record<string, { path: string; mimeType?: string }>;
  headers?: Record<string, string>;
  timeoutMs?: number;
}): Promise<T> {
  const formData = new FormData();
  formData.append(
    "operations",
    JSON.stringify({
      operationName: input.operationName,
      variables: input.variables,
      query: input.query
    })
  );
  formData.append("map", JSON.stringify(input.fileFieldMap));

  for (const [partName, filePart] of Object.entries(input.fileParts)) {
    const validated = await readValidatedLocalImageUpload(filePart.path);
    const blob = new Blob([validated.bytes], {
      type: filePart.mimeType ?? validated.mimeType
    });
    formData.append(partName, blob, validated.fileName);
  }

  const controller = new AbortController();
  const timeoutMs = input.timeoutMs ?? DEFAULT_NETWORK_TIMEOUT_MS;
  const timeoutHandle = setTimeout(() => controller.abort(), timeoutMs);

  let response: Response;
  try {
    response = await fetch(input.url, {
      method: "POST",
      headers: input.headers,
      body: formData,
      signal: controller.signal
    });
  } catch (error) {
    const timedOut = error instanceof Error && error.name === "AbortError";
    throw new Error(
      timedOut
        ? `HTTP timeout after ${timeoutMs}ms for ${input.url}`
        : `HTTP request failed for ${input.url}: ${error instanceof Error ? error.message : String(error)}`
    );
  } finally {
    clearTimeout(timeoutHandle);
  }

  let body: unknown;
  try {
    body = await response.json();
  } catch {
    body = await response.text();
  }
  if (!response.ok) {
    console.error(
      `[element-drop] external response ${JSON.stringify({
        method: "POST",
        url: input.url,
        status: response.status,
        body
      })}`
    );
    throw new Error(
      `HTTP ${response.status} for ${input.url}: ${typeof body === "string" ? body : JSON.stringify(body)}`
    );
  }

  return body as T;
}

function getGraphqlErrorMessage(response: {
  errors?: Array<{
    message?: string;
  }>;
}): string | null {
  const messages = (response.errors ?? []).map((error) => error.message).filter(Boolean);
  return messages.length > 0 ? messages.join("; ") : null;
}

export function createElementGraphqlClient(
  baseUrl = DEFAULT_ELEMENT_GRAPHQL_URL,
  auth = {
    tokenA: resolveElementGraphqlTokenA(),
    tokenB: resolveElementGraphqlTokenB()
  }
) {
  return {
    async getLoginNonce(identity: ElementIdentity): Promise<string> {
      const response = await postJson<LoginNonceResponse>(baseUrl, {
        body: {
          query: ELEMENT_LOGIN_NONCE_QUERY,
          variables: {
            address: identity.address,
            chain: identity.blockChain.chain,
            chainId: identity.blockChain.chainId
          }
        },
        headers: buildElementGraphqlGatewayHeaders(auth)
      });

      const nonce = response.data?.user?.nonce;
      if (nonce === null || nonce === undefined) {
        throw new Error(
          getGraphqlErrorMessage(response) ?? `Element login nonce missing for ${identity.address}`
        );
      }

      return String(nonce);
    },

    async loginAuth(input: ElementLoginInput): Promise<string> {
      const response = await postJson<LoginAuthResponse>(baseUrl, {
        body: {
          query: ELEMENT_LOGIN_AUTH_MUTATION,
          variables: {
            identity: input.identity,
            message: input.message,
            signature: input.signature,
            realm: input.realm,
            source: input.source
          }
        },
        headers: buildElementGraphqlGatewayHeaders(auth)
      });

      const token = response.data?.auth?.login?.token;
      if (!token) {
        throw new Error(
          getGraphqlErrorMessage(response) ?? `Element login token missing for ${input.identity.address}`
        );
      }

      return token;
    },

    async getCollectionContract(identity: ElementIdentity) {
      const response = await postJson<CollectionContractResponse>(baseUrl, {
        body: {
          operationName: "CollectionContract",
          variables: {
            address: identity.address,
            blockChain: identity.blockChain
          },
          query: COLLECTION_CONTRACT_QUERY
        },
        headers: buildElementGraphqlGatewayHeaders(auth)
      });

      return response.data?.contract?.chainCollection ?? null;
    },

    async getMutateToken(authorization?: string): Promise<string> {
      const response = await postJson<GetMutateTokenResponse>(baseUrl, {
        body: {
          operationName: "GetMutateToken",
          variables: {},
          query: GET_MUTATE_TOKEN_QUERY
        },
        headers: withOptionalAuthorization(buildElementGraphqlGatewayHeaders(auth), authorization)
      });

      const token = response.data?.mutateToken?.token;
      if (!token) {
        throw new Error(getGraphqlErrorMessage(response) ?? "Element mutate token missing");
      }

      return token;
    },

    async getCollectionDetailFromEditors(slug: string, authorization?: string) {
      const response = await postJson<CollectionDetailFromEditorsResponse>(baseUrl, {
        body: {
          operationName: "CollectionDetailFromEditors",
          variables: {
            slug
          },
          query: COLLECTION_DETAIL_FROM_EDITORS_QUERY
        },
        headers: withOptionalAuthorization(buildElementGraphqlGatewayHeaders(auth), authorization)
      });

      const collection = response.data?.collection;
      if (!collection) {
        throw new Error(
          getGraphqlErrorMessage(response) ?? `Element collection detail missing for slug ${slug}`
        );
      }

      return collection;
    },

    async collectionEdit(input: ElementCollectionEditInput, authorization?: string) {
      const headers = withOptionalAuthorization(buildElementGraphqlGatewayHeaders(auth), authorization);
      const imageFilePath = input.imageFilePath;
      const variables = {
        ...input,
        imageFilePath: undefined,
        ...(imageFilePath ? { image: null } : ("image" in input ? { image: input.image } : {}))
      };
      const response = imageFilePath
        ? await postGraphqlMultipart<CollectionEditResponse>({
            url: `${baseUrl}?args=collectionEdit`,
            operationName: "collectionEdit",
            variables,
            query: COLLECTION_EDIT_MUTATION,
            fileFieldMap: {
              "1": ["variables.image"]
            },
            fileParts: {
              "1": {
                path: imageFilePath
              }
            },
            headers
          })
        : await postJson<CollectionEditResponse>(baseUrl, {
            body: {
              operationName: "collectionEdit",
              variables,
              query: COLLECTION_EDIT_MUTATION
            },
            headers
          });

      const collection = response.data?.collections?.modify;
      if (!collection) {
        throw new Error(
          getGraphqlErrorMessage(response) ??
            `Element collection edit result missing for collection ${input.collectionId}`
        );
      }

      return collection;
    },

    async getUserCollectionList(input: {
      identity: ElementIdentity;
      first?: number;
      after?: string;
      before?: string;
      last?: number;
      authorization?: string;
    }) {
      const response = await postJson<UserCollectionListResponse>(baseUrl, {
        body: {
          operationName: "UserCollectionList",
          variables: {
            first: input.first ?? 28,
            after: input.after,
            before: input.before,
            last: input.last,
            owners: [input.identity],
            editors: [input.identity],
            blockChains: [input.identity.blockChain]
          },
          query: USER_COLLECTION_LIST_QUERY
        },
        headers: withOptionalAuthorization(buildElementGraphqlGatewayHeaders(auth), input.authorization)
      });

      const collectionSearch = response.data?.collectionSearch;
      if (!collectionSearch) {
        throw new Error(getGraphqlErrorMessage(response) ?? "Element user collection list missing");
      }

      return {
        items: (collectionSearch.edges ?? []).map((edge) => edge.node),
        pageInfo: collectionSearch.pageInfo ?? null
      };
    }
  };
}
