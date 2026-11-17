export type ParsedLog = {
  txHash: string;
  logIndex: number;
  blockNumber: number;
  eventName: string;
  data: Record<string, string | boolean>;
};
