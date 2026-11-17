import fs from 'fs';
import { ethers } from 'ethers';

import { abiJsonPath } from './paths';
import {
  buildParseLog,
  getEventTopicHash,
  listAbiEventNames,
} from './utils/parse.log';

type ContractEntry = {
  address: string;
  startBlock: number;
  endBlock: number | 'latest';
  chainId: number;
  /** One RPC URL, or ordered list for automatic failover. */
  rpc: string | string[];
  /**
   * '*' = all events; string[] = selected event names from ABI.
   */
  eventNames: '*' | string[];
  tokenDecimals?: number;
};

export type ContractsConfig = {
  contracts: Record<string, ContractEntry>;
};

function loadContractAbi(address: string, chainId: number) {
  const filePath = abiJsonPath(address, chainId);
  if (!fs.existsSync(filePath)) {
    throw new Error(`ABI not found: ${filePath}`);
  }
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

/** ← Customize after user provides chainId + address and picks events. */
export const Contracts: ContractsConfig = {
  contracts: {
    MyContract: {
      address: '0x0000000000000000000000000000000000000000',
      startBlock: 0,
      endBlock: 'latest',
      rpc: [
        'https://your-rpc.example.com',
        // 'https://backup-rpc.example.com',
      ],
      chainId: 1,
      eventNames: '*',
      tokenDecimals: 18,
    },
  },
};

/** @deprecated use Contracts */
export const Distributors = Contracts;

export const ContractConfigs = Object.entries(Contracts.contracts).map(
  ([name, cfg]) => {
    const { address, startBlock, endBlock, rpc, chainId, eventNames, tokenDecimals } =
      cfg;
    const abi = loadContractAbi(address, chainId);
    const abiInterface = new ethers.Interface(abi);
    const resolvedNames =
      eventNames === '*' ? listAbiEventNames(abiInterface) : eventNames;

    return {
      name,
      address,
      startBlock,
      endBlock,
      rpc,
      chainId,
      eventNames: resolvedNames,
      /** topic0 filter: undefined = all logs; else OR of selected event topic hashes */
      getTopics: (): (string | string[])[] => {
        if (eventNames === '*') {
          return [];
        }
        const hashes = resolvedNames.map((n) => getEventTopicHash(abiInterface, n));
        return hashes.length === 1 ? [hashes[0]] : [hashes];
      },
      parseLog: buildParseLog(abiInterface, { tokenDecimals, eventNames }),
    };
  },
);
