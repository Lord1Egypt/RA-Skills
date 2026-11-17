import { ethers } from 'ethers';
import Decimal from 'decimal.js';
import type { ParsedLog } from '../types';

function resolveEventFragment(
  abiInterface: ethers.Interface,
  eventName: string,
): ethers.EventFragment {
  const fragment =
    abiInterface.getEvent(eventName) ??
    abiInterface.getEvent(eventName.split('(')[0]);
  if (!fragment) {
    throw new Error(`Event not found in ABI: ${eventName}`);
  }
  return fragment;
}

export function getEventTopicHash(
  abiInterface: ethers.Interface,
  eventName: string,
): string {
  return resolveEventFragment(abiInterface, eventName).topicHash;
}

export function listAbiEventNames(abiInterface: ethers.Interface): string[] {
  const names: string[] = [];
  abiInterface.forEachEvent((event) => {
    names.push(event.name);
  });
  return names;
}

function normalizeEventArg(
  value: unknown,
  type: string,
  tokenDecimals?: number,
): string | boolean {
  if (type === 'address') {
    return String(value).toLowerCase();
  }
  if (type === 'bool') {
    return Boolean(value);
  }
  if (type === 'bytes32') {
    return String(value).toLowerCase();
  }
  if (type.startsWith('uint') || type.startsWith('int')) {
    const raw = new Decimal(String(value));
    if (tokenDecimals != null) {
      return raw.div(10 ** tokenDecimals).toFixed();
    }
    return raw.toFixed();
  }
  return String(value);
}

export function buildParseLog(
  abiInterface: ethers.Interface,
  options?: { tokenDecimals?: number; eventNames?: string[] | '*' },
) {
  const allowed =
    options?.eventNames == null || options.eventNames === '*'
      ? null
      : new Set(options.eventNames);

  return (rawLog: ethers.LogParams | Record<string, unknown>): ParsedLog | null => {
    const parsed = abiInterface.parseLog(rawLog as ethers.LogParams);
    if (!parsed) {
      return null;
    }
    if (allowed && !allowed.has(parsed.name)) {
      return null;
    }

    const data: Record<string, string | boolean> = {};
    for (const input of parsed.fragment.inputs) {
      if (!input.name) {
        continue;
      }
      data[input.name] = normalizeEventArg(
        parsed.args[input.name],
        input.type,
        options?.tokenDecimals,
      );
    }

    const log = rawLog as {
      transactionHash: string;
      blockNumber: number | string;
      index?: number;
      logIndex?: number | string;
    };

    return {
      txHash: log.transactionHash,
      logIndex: Number(log.index ?? log.logIndex ?? 0),
      blockNumber: Number(log.blockNumber),
      eventName: parsed.name,
      data,
    };
  };
}
