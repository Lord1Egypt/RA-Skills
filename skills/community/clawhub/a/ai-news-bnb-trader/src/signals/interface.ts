import { NewsItem, SignalResult } from '../types.js';

export interface ISignalModel {
  analyze(news: NewsItem): Promise<SignalResult>;
}
