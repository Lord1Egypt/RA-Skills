import { buildElementAuthorization, deriveWalletAddress } from "../auth/jwt";
import { getRequiredWalletPrivateKey } from "../env";
import { createElementGraphqlClient } from "../api/graphql";

export async function verifyRefGraphqlExamples() {
  const privateKey = getRequiredWalletPrivateKey();
  const walletAddress = (await deriveWalletAddress({ privateKey })).toLowerCase();
  const graphql = createElementGraphqlClient();
  const authorization = (
    await buildElementAuthorization(
      {
        getLoginNonce: graphql.getLoginNonce,
        loginAuth: graphql.loginAuth
      },
      {
        privateKey,
        walletAddress,
        chainMId: 1201
      }
    )
  ).authorization;

  const results: Record<string, unknown> = {};

  results.getNonce = await graphql.getLoginNonce({
    address: "0x00000007699893e07f12d7d35ac7e4534c31613e",
    blockChain: {
      chain: "eth",
      chainId: "0x1"
    }
  });

  results.collectionContract = await graphql.getCollectionContract({
    address: "0x7122ad8c3f90fd23cb89d3ffa5ce7feac8d64c6a",
    blockChain: {
      chain: "base",
      chainId: "0x2105"
    }
  });

  results.getMutateToken = await graphql.getMutateToken(authorization);

  results.collectionDetailFromEditors = await graphql.getCollectionDetailFromEditors(
    "1122-5",
    authorization
  );

  try {
    results.collectionEdit = await graphql.collectionEdit(
      {
        collectionId: "18829680",
        token: String(results.getMutateToken),
        image: null
      },
      authorization
    );
  } catch (error) {
    results.collectionEdit = {
      ok: false,
      error: error instanceof Error ? error.message : String(error)
    };
  }

  return {
    authorization,
    walletAddress,
    results
  };
}
