import { zeroAddress } from "viem";
import { describe, expect, it } from "vitest";

import { MAINNET, resolveNetwork, TESTNET } from "./network.js";

const mainnet = { BRAINCHAIN_NETWORK: "mainnet" };

describe("resolveNetwork", () => {
  it("keeps testnet the default", () => {
    expect(resolveNetwork({})).toEqual(TESTNET);
    expect(resolveNetwork({ BRAINCHAIN_NETWORK: " Testnet " })).toEqual(TESTNET);
  });

  it("resolves mainnet to the 3.5.0 set", () => {
    const network = resolveNetwork(mainnet);
    expect(network).toMatchObject({
      name: "BrainChain",
      chainId: 274663,
      rpc: "https://rpc.usebrainchain.com",
      service: "https://brain.usebrainchain.com",
      fromBlock: 965n,
      explorer: "https://usebrainchain.com",
      stakeSymbol: "BRAIN",
      bountySymbol: "USDG",
    });
    expect(network.contracts).toEqual({
      taskBoard: "0x44b8464342Bbfb9B565FAE494DfDefa37D33A211",
      staking: "0xa4351E2b84eb634E93D9082907B2d0D3Aa91B98F",
      bonds: "0x33260Cd6b4F368031F5AF2B5413d0CE6bb2aFAA4",
      executor: "0xFD268Ae2c1Ec0Db03C3C6b17E1AEDE973729FE29",
      gate: "0x71B2dc3dEC1aEB000936380981DfC51E47AA4fb8",
      registry: "0xA7f8A21Cc9574DB049F525a4fd499DA49c0D51ed",
      stakeToken: "0x3367085Eb6C79BfB0fCa4f1433ec77bFA8CB8a37",
      bountyToken: "0x8eBFEce96c0AeF7Fd23425D846a302a552c8c451",
      log: "0x2EF509bd9cA1e7C5FBe2C2FD7Ff25cE9F6f9cB68",
    });
    expect(network.proofs).toEqual({
      chainId: 4663,
      name: "Robinhood Chain",
      rpc: "https://rpc.mainnet.chain.robinhood.com",
      rpcFallbacks: ["https://rpc-robinhood.globalstake.io", "https://robinhood.api.pocket.network"],
      collection: "0xE6E6B7DBF1a66dFB25c6F6A87a916B3186113169",
      weth: "0x0Bd7D308f8E1639FAb988df18A8011f41EAcAD73",
      gas: "Send it a little ETH there for gas",
      income: "0xeb1b4168D4b87D3d9F0D64E13B7071251BBB63b7",
      bonds: {
        registry: "0xD5Da523ee49CB7Fe855B0C6fa38707190A9D531F",
        check: "0x2e7C4F0F2e6079C3B5F7Cd2440308234CBDc537D",
        proofIndex: "0x0fb02559e704549794EdF3FBBBe91DB88bB849ee",
        usdg: "0x5fc5360D0400a0Fd4f2af552ADD042D716F1d168",
      },
    });
    expect(resolveNetwork({ BRAINCHAIN_NETWORK: "MAINNET" })).toEqual(MAINNET);
  });

  it("refuses mainnet while any of its contracts is the zero address", () => {
    for (const contract of ["taskBoard", "staking", "bonds", "executor"] as const) {
      const unfinished = { ...MAINNET, contracts: { ...MAINNET.contracts, [contract]: zeroAddress } };
      expect(() => resolveNetwork(mainnet, unfinished)).toThrow("BrainChain mainnet is not open to outside workers yet");
      expect(resolveNetwork({}, unfinished)).toEqual(TESTNET);
    }
  });

  it("takes the RPC and service overrides on mainnet too", () => {
    const network = resolveNetwork({ ...mainnet, BRAINCHAIN_RPC_URL: "https://rpc.example.com/v2/key", BRAINCHAIN_SERVICE_URL: "https://brain.example.com/" });
    expect(network).toMatchObject({ chainId: 274663, rpc: "https://rpc.example.com/v2/key", service: "https://brain.example.com" });
  });

  it("names the networks it knows", () => {
    expect(() => resolveNetwork({ BRAINCHAIN_NETWORK: "devnet" })).toThrow('BRAINCHAIN_NETWORK must be testnet or mainnet, not "devnet"');
  });

  it("gives testnet a faucet and mainnet a place to buy the stake token", () => {
    expect(TESTNET.buyStake).toBeUndefined();
    expect(TESTNET.proofs.income).toBeUndefined();
    expect(TESTNET.proofs).toMatchObject({ chainId: 46630, collection: "0x324B52EE2182641ec29652076ab541bc9F9907d2", weth: "0x1F852eF3Afa13156b807204d838BbB46B4b452eb", faucet: true });
    expect(MAINNET.proofs.faucet).toBeUndefined();
    expect(MAINNET.buyStake).toContain("https://ripples.run/t/0xa06e3D898Bce92F67617E0Bfb640F153A5b65AB7");
  });
});

describe("the desk exit pays", () => {
  it("is pinned on both networks: the testnet service names it, and on mainnet it is the poster of tasks paid through the desk", () => {
    expect(TESTNET.exitDesk).toBe("0xf848984c8A0D9E49Cc9C97380C62b34C6f3b97D1");
    expect(MAINNET.exitDesk).toBe("0x97D558417c3D61f1074422AD843e1Db1E565b952");
  });
});
