import { ExchangeClient, HttpTransport, InfoClient } from "@nktkas/hyperliquid";
import { formatPrice, formatSize } from "@nktkas/hyperliquid/utils";
import { SymbolConverter } from "@nktkas/hyperliquid/utils";
import type { Address } from "viem";
import { appConfig } from "../config.js";
import type {
  CancelHyperliquidOrderInput,
  HyperliquidAccountStateInput,
  HyperliquidOrderSide,
  HyperliquidMarketStateInput,
  HyperliquidMarginMode,
  HyperliquidTimeInForce,
  HyperliquidTriggerKind,
  PlaceHyperliquidOrderInput,
  ProtectHyperliquidPositionInput,
  SafetyDecision
} from "../types.js";
import { readLogEvents } from "../utils/logging.js";
import { WalletService } from "./walletService.js";

interface ParsedMarketRef {
  dex?: string;
  coin: string;
  displayName: string;
}

interface DexMetadata {
  name: string;
  fullName: string;
}

interface MarketContext {
  assetIndex: number;
  dex?: string;
  coin: string;
  name: string;
  szDecimals: number;
  maxLeverage: number;
  isDelisted: boolean;
  onlyIsolated: boolean;
  marginMode?: string;
  markPx?: string;
  midPx?: string | null;
  oraclePx?: string;
  funding?: string;
  openInterest?: string;
  dayNtlVlm?: string;
}

interface SimulatedBookFill {
  averagePrice: number;
  worstPrice: number;
}

interface HyperliquidOrderQuote {
  market: string;
  assetIndex: number;
  dex?: string;
  side: "buy" | "sell";
  size: string;
  orderType: "market" | "limit";
  reduceOnly: boolean;
  leverage: number;
  marginMode: HyperliquidMarginMode;
  referencePrice: string;
  estimatedFillPrice: string;
  submissionPrice: string;
  timeInForce: HyperliquidTimeInForce | "ioc";
  slippageBps: number;
  notionalUsd: string;
  estimatedInitialMarginUsd: string;
  marketState: {
    dex?: string;
    coin: string;
    szDecimals: number;
    maxLeverage: number;
    isDelisted: boolean;
    onlyIsolated: boolean;
    funding?: string;
    openInterest?: string;
    dayNtlVlm?: string;
    markPx?: string;
    midPx?: string | null;
    oraclePx?: string;
  };
  book?: {
    bestBid?: string;
    bestAsk?: string;
    simulatedAverageFillPrice: string;
    simulatedWorstLevelPrice: string;
  };
  accountState: {
    user: Address;
    dex?: string;
    abstractionState: string;
    dexAbstractionEnabled?: boolean | null;
    accountValue: string;
    withdrawable: string;
    totalMarginUsed: string;
    openOrdersCount: number;
    positionCount: number;
  };
  safety: SafetyDecision;
}

interface HyperliquidPositionContext {
  market: string;
  coin: string;
  side: "long" | "short";
  size: string;
  absoluteSize: string;
  entryPx: string;
  liquidationPx?: string;
  marginUsed: string;
  unrealizedPnl: string;
  returnOnEquity: string;
  leverage: {
    type: string;
    value: number;
    rawUsd?: string;
  };
  maxLeverage: number;
}

interface HyperliquidProtectionOrderPreview {
  kind: HyperliquidTriggerKind;
  closeSide: "buy" | "sell";
  size: string;
  triggerPx: string;
  submissionPrice: string;
  adjustedForLiquidation: boolean;
}

interface HyperliquidProtectionQuote {
  market: string;
  assetIndex: number;
  dex?: string;
  grouping: "na";
  replaceExisting: boolean;
  liquidationBufferBps: number;
  position: HyperliquidPositionContext;
  takeProfit: HyperliquidProtectionOrderPreview;
  stopLoss: HyperliquidProtectionOrderPreview;
  accountState: {
    user: Address;
    dex?: string;
    abstractionState: string;
    dexAbstractionEnabled?: boolean | null;
    accountValue: string;
    withdrawable: string;
    totalMarginUsed: string;
    openOrdersCount: number;
    positionCount: number;
  };
  existingReduceOnlyOrders: Array<{
    orderId: number;
    side: "buy" | "sell";
    size: string;
    price: string;
    reduceOnly: boolean;
    isTrigger?: boolean;
    triggerPx?: string;
  }>;
  safety: SafetyDecision;
}

function formatDisplayMarket(dex: string | undefined, coin: string): string {
  if (coin.includes(":")) {
    const [rawDex, rawCoin] = coin.split(":");
    return `${rawDex}:${rawCoin?.toUpperCase() ?? ""}`;
  }

  return dex ? `${dex}:${coin.toUpperCase()}` : coin.toUpperCase();
}

function formatNumber(value: number, maxDecimals = 8): string {
  const normalized = value.toFixed(maxDecimals);
  return normalized.replace(/\.?0+$/, "") || "0";
}

function toNumber(value: string | null | undefined): number {
  if (!value) {
    return 0;
  }

  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : 0;
}

export class HyperliquidTradingService {
  private readonly transport = new HttpTransport({
    apiUrl: appConfig.hyperliquid.apiUrl
  });

  private readonly infoClient = new InfoClient({
    transport: this.transport
  });

  public constructor(private readonly walletService: WalletService) {}

  public async getMarketState(input: HyperliquidMarketStateInput): Promise<Record<string, unknown>> {
    this.assertTradingEnabled();

    if (input.market) {
      const market = await this.getMarketByReference(input.market);
      const book = await this.infoClient.l2Book(this.withDex({ coin: market.name }, market.dex));
      return {
        market: market.name,
        dex: market.dex,
        coin: market.coin,
        assetIndex: market.assetIndex,
        szDecimals: market.szDecimals,
        maxLeverage: market.maxLeverage,
        isDelisted: market.isDelisted,
        onlyIsolated: market.onlyIsolated,
        funding: market.funding,
        openInterest: market.openInterest,
        dayNtlVlm: market.dayNtlVlm,
        markPx: market.markPx,
        midPx: market.midPx,
        oraclePx: market.oraclePx,
        bestBid: book?.levels[0]?.[0]?.px,
        bestAsk: book?.levels[1]?.[0]?.px,
        bookTimestamp: book?.time
      };
    }

    const [universe, dexes] = await Promise.all([this.getUniverse(), this.getPerpDexCatalog()]);
    return {
      marketCount: universe.length,
      availableDexs: dexes,
      markets: universe.map((market) => ({
        market: market.name,
        dex: market.dex,
        coin: market.coin,
        assetIndex: market.assetIndex,
        szDecimals: market.szDecimals,
        maxLeverage: market.maxLeverage,
        isDelisted: market.isDelisted,
        onlyIsolated: market.onlyIsolated,
        funding: market.funding,
        openInterest: market.openInterest,
        dayNtlVlm: market.dayNtlVlm,
        markPx: market.markPx,
        midPx: market.midPx,
        oraclePx: market.oraclePx
      }))
    };
  }

  public async getAccountState(input: HyperliquidAccountStateInput): Promise<Record<string, unknown>> {
    this.assertTradingEnabled();
    const user = this.resolveUserAddress(input.user);
    const dex = await this.resolveDexName(input.dex);
    const [accountState, openOrders, abstractionState, dexAbstractionEnabled] = await Promise.all([
      this.infoClient.clearinghouseState(this.withDex({ user }, dex)),
      this.infoClient.openOrders(this.withDex({ user }, dex)),
      this.infoClient.userAbstraction({ user }),
      this.infoClient.userDexAbstraction({ user })
    ]);

    return {
      user,
      dex,
      abstractionState,
      dexAbstractionEnabled,
      marginSummary: accountState.marginSummary,
      crossMarginSummary: accountState.crossMarginSummary,
      withdrawable: accountState.withdrawable,
      crossMaintenanceMarginUsed: accountState.crossMaintenanceMarginUsed,
      positions: accountState.assetPositions.map((item) => ({
        market: formatDisplayMarket(dex, item.position.coin),
        coin: item.position.coin,
        size: item.position.szi,
        entryPx: item.position.entryPx,
        positionValue: item.position.positionValue,
        unrealizedPnl: item.position.unrealizedPnl,
        returnOnEquity: item.position.returnOnEquity,
        liquidationPx: item.position.liquidationPx,
        marginUsed: item.position.marginUsed,
        leverage: item.position.leverage,
        maxLeverage: item.position.maxLeverage
      })),
      openOrders: openOrders.map((order) => ({
        market: formatDisplayMarket(dex, order.coin),
        coin: order.coin,
        side: order.side === "B" ? "buy" : "sell",
        price: order.limitPx,
        size: order.sz,
        originalSize: order.origSz,
        orderId: order.oid,
        timestamp: order.timestamp,
        reduceOnly: Boolean(order.reduceOnly),
        cloid: order.cloid
      }))
    };
  }

  public async quoteOrder(input: PlaceHyperliquidOrderInput): Promise<HyperliquidOrderQuote> {
    this.assertTradingEnabled();
    const market = await this.getMarketByReference(input.market);
    this.assertTradableMarket(market);
    this.assertSizePrecision(input.size, market.szDecimals);

    const user = this.resolveUserAddress(input.accountAddress);
    const [accountState, openOrders, abstractionState, dexAbstractionEnabled] = await Promise.all([
      this.infoClient.clearinghouseState(this.withDex({ user }, market.dex)),
      this.infoClient.openOrders(this.withDex({ user }, market.dex)),
      this.infoClient.userAbstraction({ user }),
      market.dex ? this.infoClient.userDexAbstraction({ user }) : Promise.resolve(null)
    ]);

    const referencePrice = this.getReferencePrice(market);
    const reduceOnly = input.reduceOnly ?? false;
    const leverage = input.leverage ?? 1;
    const marginMode = input.marginMode ?? (market.onlyIsolated ? "isolated" : "cross");

    const normalizedSize = formatSize(input.size, market.szDecimals);
    const size = Number(normalizedSize);
    if (!Number.isFinite(size) || size <= 0) {
      throw new Error("size must be a positive decimal string.");
    }

    let estimatedFillPrice = referencePrice;
    let submissionPrice = input.price ? Number(input.price) : referencePrice;
    let bookSummary: HyperliquidOrderQuote["book"];
    let effectiveSlippageBps = input.slippageBps ?? appConfig.hyperliquidTrading.defaultSlippageBps;
    let effectiveTimeInForce: HyperliquidOrderQuote["timeInForce"] = input.timeInForce ?? "gtc";

    if (input.orderType === "market") {
      const book = await this.infoClient.l2Book(this.withDex({ coin: market.name }, market.dex));
      if (!book) {
        throw new Error(`Unable to load L2 book for ${market.name}.`);
      }

      const simulated = this.simulateBookFill(book.levels, input.side, size);
      estimatedFillPrice = simulated.averagePrice;
      submissionPrice = input.side === "buy"
        ? simulated.worstPrice * (1 + effectiveSlippageBps / 10_000)
        : Math.max(simulated.worstPrice * (1 - effectiveSlippageBps / 10_000), 0.00000001);
      effectiveTimeInForce = "ioc";
      bookSummary = {
        bestBid: book.levels[0]?.[0]?.px,
        bestAsk: book.levels[1]?.[0]?.px,
        simulatedAverageFillPrice: formatNumber(simulated.averagePrice),
        simulatedWorstLevelPrice: formatNumber(simulated.worstPrice)
      };
    } else {
      submissionPrice = Number(input.price);
      estimatedFillPrice = submissionPrice;
      effectiveSlippageBps = input.slippageBps ?? 0;
    }

    const notionalUsd = size * estimatedFillPrice;
    const accountValue = toNumber(accountState.marginSummary.accountValue);
    const withdrawable = toNumber(accountState.withdrawable);
    const estimatedInitialMarginUsd = reduceOnly ? 0 : notionalUsd / Math.max(leverage, 1);
    const formattedSubmissionPrice = formatPrice(submissionPrice, market.szDecimals, "perp");

    const safety = this.evaluateOrderSafety({
      market,
      notionalUsd,
      leverage,
      reduceOnly,
      approval: input.approval,
      accountValue,
      withdrawable,
      estimatedInitialMarginUsd
    });

    if (market.dex) {
      this.applyDexAbstractionSafety(safety, {
        market,
        abstractionState,
        dexAbstractionEnabled,
        enableDexAbstraction: input.enableDexAbstraction
      });
    }

    return {
      market: market.name,
      assetIndex: market.assetIndex,
      dex: market.dex,
      side: input.side,
      size: normalizedSize,
      orderType: input.orderType,
      reduceOnly,
      leverage,
      marginMode,
      referencePrice: formatNumber(referencePrice),
      estimatedFillPrice: formatNumber(estimatedFillPrice),
      submissionPrice: formattedSubmissionPrice,
      timeInForce: effectiveTimeInForce,
      slippageBps: effectiveSlippageBps,
      notionalUsd: formatNumber(notionalUsd, 2),
      estimatedInitialMarginUsd: formatNumber(estimatedInitialMarginUsd, 2),
      marketState: {
        dex: market.dex,
        coin: market.coin,
        szDecimals: market.szDecimals,
        maxLeverage: market.maxLeverage,
        isDelisted: market.isDelisted,
        onlyIsolated: market.onlyIsolated,
        funding: market.funding,
        openInterest: market.openInterest,
        dayNtlVlm: market.dayNtlVlm,
        markPx: market.markPx,
        midPx: market.midPx,
        oraclePx: market.oraclePx
      },
      book: bookSummary,
      accountState: {
        user,
        dex: market.dex,
        abstractionState,
        dexAbstractionEnabled,
        accountValue: accountState.marginSummary.accountValue,
        withdrawable: accountState.withdrawable,
        totalMarginUsed: accountState.marginSummary.totalMarginUsed,
        openOrdersCount: openOrders.length,
        positionCount: accountState.assetPositions.length
      },
      safety
    };
  }

  public async placeOrder(input: PlaceHyperliquidOrderInput): Promise<Record<string, unknown>> {
    const quote = await this.quoteOrder(input);
    const user = input.accountAddress ?? this.walletService.getTreasuryAddress();
    if (user.toLowerCase() !== this.walletService.getTreasuryAddress().toLowerCase()) {
      throw new Error("Execution is only supported when accountAddress matches the treasury signer address.");
    }

    const exchangeClient = this.getExchangeClient();
    let abstractionUpdate;
    if (quote.dex && quote.accountState.abstractionState !== "dexAbstraction") {
      if (!input.enableDexAbstraction) {
        throw new Error(
          `HIP-3 dex abstraction is not enabled for ${quote.dex}. Re-run with enableDexAbstraction=true after reviewing the abstraction change.`
        );
      }

      abstractionUpdate = await exchangeClient.userSetAbstraction({
        user,
        abstraction: "dexAbstraction"
      });
    }

    const leverageUpdate = input.leverage && !quote.reduceOnly
      ? await exchangeClient.updateLeverage({
          asset: quote.assetIndex,
          isCross: quote.marginMode !== "isolated",
          leverage: quote.leverage
        })
      : undefined;

    const orderResponse = await exchangeClient.order({
      orders: [
        {
          a: quote.assetIndex,
          b: quote.side === "buy",
          p: quote.submissionPrice,
          s: quote.size,
          r: quote.reduceOnly,
          t: {
            limit: {
              tif: this.toSdkTimeInForce(quote.timeInForce, quote.orderType)
            }
          }
        }
      ],
      grouping: "na"
    });

    return {
      quote,
      abstractionUpdate,
      leverageUpdate,
      response: orderResponse
    };
  }

  public async quoteProtection(input: ProtectHyperliquidPositionInput): Promise<HyperliquidProtectionQuote> {
    this.assertTradingEnabled();
    const market = await this.getMarketByReference(input.market);
    this.assertTradableMarket(market);

    const user = this.resolveUserAddress(input.accountAddress);
    const [accountState, openOrders, abstractionState, dexAbstractionEnabled] = await Promise.all([
      this.infoClient.clearinghouseState(this.withDex({ user }, market.dex)),
      this.infoClient.openOrders(this.withDex({ user }, market.dex)),
      this.infoClient.userAbstraction({ user }),
      market.dex ? this.infoClient.userDexAbstraction({ user }) : Promise.resolve(null)
    ]);

    const position = this.extractPositionContext(accountState.assetPositions, market);
    const takeProfitRoePercent = input.takeProfitRoePercent ?? 100;
    const stopLossRoePercent = input.stopLossRoePercent ?? 50;
    const liquidationBufferBps = input.liquidationBufferBps ?? 25;
    const closeSide: HyperliquidOrderSide = position.side === "long" ? "sell" : "buy";

    const takeProfitTriggerPx = this.computeProtectionTriggerPrice(position, takeProfitRoePercent, "tp");
    const stopLossDerived = this.computeProtectionTriggerPrice(position, stopLossRoePercent, "sl");
    const adjustedStopLoss = this.adjustStopLossTriggerForLiquidation(position, stopLossDerived, liquidationBufferBps);

    const takeProfit = this.buildProtectionOrderPreview({
      market,
      kind: "tp",
      closeSide,
      size: position.absoluteSize,
      triggerPx: takeProfitTriggerPx,
      adjustedForLiquidation: false
    });
    const stopLoss = this.buildProtectionOrderPreview({
      market,
      kind: "sl",
      closeSide,
      size: position.absoluteSize,
      triggerPx: adjustedStopLoss.triggerPx,
      adjustedForLiquidation: adjustedStopLoss.adjusted
    });

    const existingReduceOnlyOrders = openOrders
      .filter((order) => this.orderMatchesMarket(order.coin, market))
      .filter((order) => Boolean(order.reduceOnly))
      .map((order) => ({
        orderId: order.oid,
        side: order.side === "B" ? ("buy" as const) : ("sell" as const),
        size: order.sz,
        price: order.limitPx,
        reduceOnly: Boolean(order.reduceOnly)
      }));

    const notionalUsd = Math.abs(toNumber(position.absoluteSize) * toNumber(position.entryPx));
    const safety = this.evaluateOrderSafety({
      market,
      notionalUsd,
      leverage: position.leverage.value,
      reduceOnly: true,
      approval: input.approval,
      accountValue: toNumber(accountState.marginSummary.accountValue),
      withdrawable: toNumber(accountState.withdrawable),
      estimatedInitialMarginUsd: 0
    });

    if (market.dex) {
      this.applyDexAbstractionSafety(safety, {
        market,
        abstractionState,
        dexAbstractionEnabled,
        enableDexAbstraction: input.enableDexAbstraction
      });
    }

    if (stopLoss.adjustedForLiquidation) {
      safety.warnings.push(
        `Stop-loss trigger was tightened from ${formatNumber(stopLossDerived)} to ${stopLoss.triggerPx} because the requested threshold would be beyond liquidation ${position.liquidationPx}.`
      );
    }

    if (existingReduceOnlyOrders.length > 0 && !input.replaceExisting) {
      safety.warnings.push(
        `${existingReduceOnlyOrders.length} reduce-only open order(s) already exist for ${market.name}. Re-run with replaceExisting=true to replace them cleanly.`
      );
    }

    return {
      market: market.name,
      assetIndex: market.assetIndex,
      dex: market.dex,
      grouping: "na",
      replaceExisting: input.replaceExisting ?? false,
      liquidationBufferBps,
      position,
      takeProfit,
      stopLoss,
      accountState: {
        user,
        dex: market.dex,
        abstractionState,
        dexAbstractionEnabled,
        accountValue: accountState.marginSummary.accountValue,
        withdrawable: accountState.withdrawable,
        totalMarginUsed: accountState.marginSummary.totalMarginUsed,
        openOrdersCount: openOrders.length,
        positionCount: accountState.assetPositions.length
      },
      existingReduceOnlyOrders,
      safety
    };
  }

  public async protectPosition(input: ProtectHyperliquidPositionInput): Promise<Record<string, unknown>> {
    const quote = await this.quoteProtection(input);
    const user = input.accountAddress ?? this.walletService.getTreasuryAddress();
    if (user.toLowerCase() !== this.walletService.getTreasuryAddress().toLowerCase()) {
      throw new Error("Execution is only supported when accountAddress matches the treasury signer address.");
    }

    const exchangeClient = this.getExchangeClient();
    let abstractionUpdate;
    if (quote.dex && quote.accountState.abstractionState !== "dexAbstraction") {
      if (!input.enableDexAbstraction) {
        throw new Error(
          `HIP-3 dex abstraction is not enabled for ${quote.dex}. Re-run with enableDexAbstraction=true after reviewing the abstraction change.`
        );
      }

      abstractionUpdate = await exchangeClient.userSetAbstraction({
        user,
        abstraction: "dexAbstraction"
      });
    }

    const canceledOrders = [];
    if (input.replaceExisting && quote.existingReduceOnlyOrders.length > 0) {
      for (const order of quote.existingReduceOnlyOrders) {
        const cancelResponse = await exchangeClient.cancel({
          cancels: [
            {
              a: quote.assetIndex,
              o: order.orderId
            }
          ]
        });
        canceledOrders.push({
          order,
          response: cancelResponse
        });
      }
    }

    const response = await exchangeClient.order({
      orders: [
        this.buildTriggerSdkOrder(quote.assetIndex, quote.takeProfit),
        this.buildTriggerSdkOrder(quote.assetIndex, quote.stopLoss)
      ],
      grouping: quote.grouping
    });

    return {
      quote,
      abstractionUpdate,
      canceledOrders,
      response
    };
  }

  public async previewCancel(input: CancelHyperliquidOrderInput): Promise<Record<string, unknown>> {
    this.assertTradingEnabled();
    const user = this.resolveUserAddress();
    const market = await this.getMarketByReference(input.market);
    const [openOrders, abstractionState] = await Promise.all([
      this.infoClient.openOrders(this.withDex({ user }, market.dex)),
      market.dex ? this.infoClient.userAbstraction({ user }) : Promise.resolve("default" as const)
    ]);

    const matchedOrder = openOrders.find((order) =>
      order.oid === input.orderId &&
      (
        order.coin.toUpperCase() === market.coin.toUpperCase() ||
        order.coin.toUpperCase() === market.name.toUpperCase()
      )
    );

    if (!matchedOrder) {
      throw new Error(`Open order ${input.orderId} for ${market.name} was not found.`);
    }

    return {
      user,
      market: market.name,
      dex: market.dex,
      abstractionState,
      assetIndex: market.assetIndex,
      order: {
        orderId: matchedOrder.oid,
        side: matchedOrder.side === "B" ? "buy" : "sell",
        price: matchedOrder.limitPx,
        size: matchedOrder.sz,
        originalSize: matchedOrder.origSz,
        reduceOnly: Boolean(matchedOrder.reduceOnly),
        timestamp: matchedOrder.timestamp
      }
    };
  }

  public async cancelOrder(input: CancelHyperliquidOrderInput): Promise<Record<string, unknown>> {
    const preview = await this.previewCancel(input);
    if (preview.dex && preview.abstractionState !== "dexAbstraction") {
      throw new Error(`Canceling HIP-3 orders requires dexAbstraction to be enabled for ${preview.dex}.`);
    }

    const exchangeClient = this.getExchangeClient();
    const response = await exchangeClient.cancel({
      cancels: [
        {
          a: preview.assetIndex as number,
          o: input.orderId
        }
      ]
    });

    return {
      ...preview,
      response
    };
  }

  private assertTradingEnabled(): void {
    if (!appConfig.hyperliquidTrading.enabled) {
      throw new Error("Hyperliquid trading is disabled by configuration.");
    }
  }

  private getExchangeClient() {
    return new ExchangeClient({
      transport: this.transport,
      wallet: this.walletService.requireAccount()
    });
  }

  private withDex<T extends Record<string, unknown>>(params: T = {} as T, dex?: string): T & { dex?: string } {
    const effectiveDex = dex ?? appConfig.hyperliquid.dex;
    if (!effectiveDex) {
      return params;
    }

    return {
      ...params,
      dex: effectiveDex
    };
  }

  private resolveUserAddress(user?: Address): Address {
    return user ?? this.walletService.getTreasuryAddress();
  }

  private parseMarketReference(market: string): ParsedMarketRef {
    const trimmed = market.trim();
    if (!trimmed) {
      throw new Error("market is required.");
    }

    if (trimmed.includes(":")) {
      const [rawDex, rawCoin] = trimmed.split(":");
      if (!rawDex || !rawCoin) {
        throw new Error(`Invalid HIP-3 market reference "${market}". Use "dex:COIN".`);
      }

      return {
        dex: rawDex.trim(),
        coin: rawCoin.trim().toUpperCase(),
        displayName: `${rawDex.trim()}:${rawCoin.trim().toUpperCase()}`
      };
    }

    const configuredDex = appConfig.hyperliquid.dex;
    return {
      dex: configuredDex,
      coin: trimmed.toUpperCase(),
      displayName: configuredDex ? `${configuredDex}:${trimmed.toUpperCase()}` : trimmed.toUpperCase()
    };
  }

  private async getPerpDexCatalog(): Promise<DexMetadata[]> {
    const dexes = await this.infoClient.perpDexs();
    return dexes
      .filter((item): item is NonNullable<typeof item> => item !== null)
      .map((item) => ({
        name: item.name,
        fullName: item.fullName
      }));
  }

  private async resolveDexName(dex?: string): Promise<string | undefined> {
    const requested = dex?.trim() || appConfig.hyperliquid.dex;
    if (!requested) {
      return undefined;
    }

    const dexes = await this.getPerpDexCatalog();
    const matched = dexes.find((item) => item.name.toLowerCase() === requested.toLowerCase());
    if (!matched) {
      throw new Error(`Hyperliquid HIP-3 dex "${requested}" was not found.`);
    }

    return matched.name;
  }

  private async getUniverse(dex?: string): Promise<MarketContext[]> {
    const resolvedDex = await this.resolveDexName(dex);
    const [meta, assetCtxs] = await this.infoClient.metaAndAssetCtxs(this.withDex({}, resolvedDex));
    const converter = await SymbolConverter.create({
      transport: this.transport,
      dexs: resolvedDex ? [resolvedDex] : false
    });

    return meta.universe.map((entry, index) => {
      const displayName = formatDisplayMarket(resolvedDex, entry.name);
      const assetIndex = resolvedDex
        ? converter.getAssetId(displayName)
        : index;

      if (assetIndex === undefined) {
        throw new Error(`Unable to resolve Hyperliquid asset id for ${displayName}.`);
      }

      return {
        assetIndex,
        dex: resolvedDex,
        coin: entry.name.includes(":") ? entry.name.split(":")[1]!.toUpperCase() : entry.name.toUpperCase(),
        name: displayName,
        szDecimals: entry.szDecimals,
        maxLeverage: entry.maxLeverage,
        isDelisted: entry.isDelisted === true,
        onlyIsolated: entry.onlyIsolated === true || entry.marginMode === "strictIsolated",
        marginMode: entry.marginMode,
        markPx: assetCtxs[index]?.markPx,
        midPx: assetCtxs[index]?.midPx,
        oraclePx: assetCtxs[index]?.oraclePx,
        funding: assetCtxs[index]?.funding,
        openInterest: assetCtxs[index]?.openInterest,
        dayNtlVlm: assetCtxs[index]?.dayNtlVlm
      };
    });
  }

  private async getMarketByReference(market: string): Promise<MarketContext> {
    const parsed = this.parseMarketReference(market);
    const universe = await this.getUniverse(parsed.dex);
    const matched = universe.find((entry) => entry.coin.toUpperCase() === parsed.coin.toUpperCase());
    if (!matched) {
      throw new Error(`Hyperliquid perpetual market ${parsed.displayName} is not available.`);
    }

    return matched;
  }

  private assertTradableMarket(market: MarketContext): void {
    if (market.isDelisted) {
      throw new Error(`${market.name} is delisted on Hyperliquid.`);
    }
  }

  private assertSizePrecision(size: string, szDecimals: number): void {
    const [, fraction = ""] = size.split(".");
    if (fraction.length > szDecimals) {
      throw new Error(`Size precision for this market is limited to ${szDecimals} decimal places.`);
    }
  }

  private getReferencePrice(market: MarketContext): number {
    const price = toNumber(market.midPx) || toNumber(market.markPx) || toNumber(market.oraclePx);
    if (!price || !Number.isFinite(price) || price <= 0) {
      throw new Error(`Unable to derive reference price for ${market.name}.`);
    }

    return price;
  }

  private extractPositionContext(assetPositions: Array<{ position: Record<string, unknown> }>, market: MarketContext): HyperliquidPositionContext {
    const matched = assetPositions.find((item) => this.orderMatchesMarket(String(item.position.coin ?? ""), market));
    if (!matched) {
      throw new Error(`No open position found for ${market.name}.`);
    }

    const size = String(matched.position.szi ?? "0");
    const numericSize = Number(size);
    if (!Number.isFinite(numericSize) || numericSize === 0) {
      throw new Error(`No open position found for ${market.name}.`);
    }

    const leverageValue = Number(
      typeof matched.position.leverage === "object" && matched.position.leverage !== null
        ? (matched.position.leverage as Record<string, unknown>).value
        : 0
    );

    return {
      market: market.name,
      coin: market.coin,
      side: numericSize > 0 ? "long" : "short",
      size,
      absoluteSize: formatNumber(Math.abs(numericSize), market.szDecimals),
      entryPx: String(matched.position.entryPx ?? "0"),
      liquidationPx: matched.position.liquidationPx ? String(matched.position.liquidationPx) : undefined,
      marginUsed: String(matched.position.marginUsed ?? "0"),
      unrealizedPnl: String(matched.position.unrealizedPnl ?? "0"),
      returnOnEquity: String(matched.position.returnOnEquity ?? "0"),
      leverage: {
        type: String(
          typeof matched.position.leverage === "object" && matched.position.leverage !== null
            ? (matched.position.leverage as Record<string, unknown>).type ?? "unknown"
            : "unknown"
        ),
        value: leverageValue,
        rawUsd:
          typeof matched.position.leverage === "object" && matched.position.leverage !== null
            ? String((matched.position.leverage as Record<string, unknown>).rawUsd ?? "")
            : undefined
      },
      maxLeverage: Number(matched.position.maxLeverage ?? market.maxLeverage)
    };
  }

  private computeProtectionTriggerPrice(
    position: HyperliquidPositionContext,
    roePercent: number,
    kind: HyperliquidTriggerKind
  ): number {
    const entryPx = toNumber(position.entryPx);
    const leverage = position.leverage.value;
    if (!entryPx || !leverage) {
      throw new Error(`Unable to derive trigger price for ${position.market}.`);
    }

    const moveFraction = (roePercent / 100) / leverage;
    if (position.side === "long") {
      return kind === "tp"
        ? entryPx * (1 + moveFraction)
        : entryPx * (1 - moveFraction);
    }

    return kind === "tp"
      ? entryPx * (1 - moveFraction)
      : entryPx * (1 + moveFraction);
  }

  private adjustStopLossTriggerForLiquidation(
    position: HyperliquidPositionContext,
    desiredTriggerPx: number,
    liquidationBufferBps: number
  ): { triggerPx: number; adjusted: boolean } {
    const liquidationPx = toNumber(position.liquidationPx);
    if (!liquidationPx) {
      return {
        triggerPx: desiredTriggerPx,
        adjusted: false
      };
    }

    if (position.side === "long") {
      const minimumSafeTrigger = liquidationPx * (1 + liquidationBufferBps / 10_000);
      if (desiredTriggerPx <= minimumSafeTrigger) {
        return {
          triggerPx: minimumSafeTrigger,
          adjusted: true
        };
      }

      return {
        triggerPx: desiredTriggerPx,
        adjusted: false
      };
    }

    const maximumSafeTrigger = liquidationPx * Math.max(1 - liquidationBufferBps / 10_000, 0.0001);
    if (desiredTriggerPx >= maximumSafeTrigger) {
      return {
        triggerPx: maximumSafeTrigger,
        adjusted: true
      };
    }

    return {
      triggerPx: desiredTriggerPx,
      adjusted: false
    };
  }

  private buildProtectionOrderPreview(args: {
    market: MarketContext;
    kind: HyperliquidTriggerKind;
    closeSide: HyperliquidOrderSide;
    size: string;
    triggerPx: number;
    adjustedForLiquidation: boolean;
  }): HyperliquidProtectionOrderPreview {
    const submissionPrice = this.getTriggerMarketSubmissionPrice(args.triggerPx, args.closeSide);
    return {
      kind: args.kind,
      closeSide: args.closeSide,
      size: args.size,
      triggerPx: formatPrice(args.triggerPx, args.market.szDecimals, "perp"),
      submissionPrice: formatPrice(submissionPrice, args.market.szDecimals, "perp"),
      adjustedForLiquidation: args.adjustedForLiquidation
    };
  }

  private getTriggerMarketSubmissionPrice(triggerPx: number, closeSide: HyperliquidOrderSide): number {
    const slippageFraction = 0.1;
    return closeSide === "buy"
      ? triggerPx * (1 + slippageFraction)
      : Math.max(triggerPx * (1 - slippageFraction), 0.00000001);
  }

  private buildTriggerSdkOrder(assetIndex: number, preview: HyperliquidProtectionOrderPreview) {
    return {
      a: assetIndex,
      b: preview.closeSide === "buy",
      p: preview.submissionPrice,
      s: preview.size,
      r: true,
      t: {
        trigger: {
          isMarket: true,
          triggerPx: preview.triggerPx,
          tpsl: preview.kind
        }
      }
    };
  }

  private orderMatchesMarket(orderCoin: string, market: MarketContext): boolean {
    const normalizedOrderCoin = orderCoin.toUpperCase();
    return normalizedOrderCoin === market.coin.toUpperCase() || normalizedOrderCoin === market.name.toUpperCase();
  }

  private simulateBookFill(
    levels: [bids: Array<{ px: string; sz: string }>, asks: Array<{ px: string; sz: string }>],
    side: "buy" | "sell",
    requestedSize: number
  ): SimulatedBookFill {
    const sideLevels = side === "buy" ? levels[1] : levels[0];
    let remaining = requestedSize;
    let totalNotionalUsd = 0;
    let worstPrice = 0;

    for (const level of sideLevels) {
      if (remaining <= 0) {
        break;
      }

      const levelSize = Number(level.sz);
      const levelPrice = Number(level.px);
      if (!Number.isFinite(levelSize) || !Number.isFinite(levelPrice) || levelSize <= 0 || levelPrice <= 0) {
        continue;
      }

      const fillSize = Math.min(remaining, levelSize);
      totalNotionalUsd += fillSize * levelPrice;
      remaining -= fillSize;
      worstPrice = levelPrice;
    }

    if (remaining > 1e-9) {
      throw new Error("Insufficient order book liquidity to simulate the requested market order.");
    }

    return {
      averagePrice: totalNotionalUsd / requestedSize,
      worstPrice
    };
  }

  private evaluateOrderSafety(args: {
    market: MarketContext;
    notionalUsd: number;
    leverage: number;
    reduceOnly: boolean;
    approval?: boolean;
    accountValue: number;
    withdrawable: number;
    estimatedInitialMarginUsd: number;
  }): SafetyDecision {
    const reasons: string[] = [];
    const warnings: string[] = [];
    const policy = appConfig.hyperliquidTrading;
    const dailyUsed = this.getDailyOrderNotionalUsed();

    if (policy.allowedMarkets.length > 0) {
      const normalizedNames = [args.market.name.toUpperCase(), args.market.coin.toUpperCase()];
      if (!normalizedNames.some((name) => policy.allowedMarkets.includes(name))) {
        reasons.push(`Market ${args.market.name} is not in the configured Hyperliquid allowlist.`);
      }
    }

    if (args.market.onlyIsolated && args.leverage > 0 && args.market.marginMode === "strictIsolated") {
      warnings.push(`${args.market.name} uses isolated-only constraints on Hyperliquid.`);
    }

    if (!args.reduceOnly && args.leverage > policy.maxLeverage) {
      reasons.push(
        `Requested leverage ${args.leverage} exceeds configured limit ${policy.maxLeverage}.`
      );
    }

    if (!args.reduceOnly && args.leverage > args.market.maxLeverage) {
      reasons.push(
        `Requested leverage ${args.leverage} exceeds market max leverage ${args.market.maxLeverage}.`
      );
    }

    if (!args.reduceOnly) {
      if (args.notionalUsd > policy.maxOrderNotionalUsd) {
        reasons.push(
          `Order notional ${formatNumber(args.notionalUsd, 2)} USD exceeds configured max ${policy.maxOrderNotionalUsd} USD.`
        );
      }

      if (dailyUsed + args.notionalUsd > policy.maxDailyOrderNotionalUsd) {
        reasons.push(
          `Daily Hyperliquid order notional would exceed limit. Used ${formatNumber(dailyUsed, 2)} USD, requested ${formatNumber(args.notionalUsd, 2)} USD, limit ${policy.maxDailyOrderNotionalUsd} USD.`
        );
      }

      if (args.notionalUsd > policy.confirmationThresholdUsd && !args.approval) {
        reasons.push(
          `Order notional ${formatNumber(args.notionalUsd, 2)} USD exceeds confirmation threshold ${policy.confirmationThresholdUsd} USD. Explicit approval=true is required.`
        );
      }

      if (args.estimatedInitialMarginUsd > args.withdrawable) {
        warnings.push(
          `Estimated initial margin ${formatNumber(args.estimatedInitialMarginUsd, 2)} USD is above withdrawable collateral ${formatNumber(args.withdrawable, 2)} USD. Hyperliquid may reject the order.`
        );
      }

      if (args.accountValue > 0 && args.notionalUsd > args.accountValue * Math.max(args.leverage, 1)) {
        warnings.push(
          `Order notional is large relative to current account value ${formatNumber(args.accountValue, 2)} USD.`
        );
      }
    }

    return {
      approved: reasons.length === 0,
      decision: reasons.length === 0 ? "approve" : "reject",
      reasons,
      warnings,
      policySnapshot: {
        allowedMarkets: policy.allowedMarkets,
        maxOrderNotionalUsd: policy.maxOrderNotionalUsd,
        maxDailyOrderNotionalUsd: policy.maxDailyOrderNotionalUsd,
        dailyUsedUsd: formatNumber(dailyUsed, 2),
        confirmationThresholdUsd: policy.confirmationThresholdUsd,
        maxLeverage: policy.maxLeverage,
        marketMaxLeverage: args.market.maxLeverage
      }
    };
  }

  private applyDexAbstractionSafety(
    safety: SafetyDecision,
    args: {
      market: MarketContext;
      abstractionState: string;
      dexAbstractionEnabled?: boolean | null;
      enableDexAbstraction?: boolean;
    }
  ): void {
    if (!args.market.dex) {
      return;
    }

    if (args.abstractionState === "dexAbstraction" || args.dexAbstractionEnabled === true) {
      safety.policySnapshot.dex = args.market.dex;
      safety.policySnapshot.requiresDexAbstraction = false;
      return;
    }

    safety.policySnapshot.dex = args.market.dex;
    safety.policySnapshot.requiresDexAbstraction = true;
    if (args.enableDexAbstraction) {
      safety.warnings.push(
        `Executing ${args.market.name} will first switch the account abstraction mode to dexAbstraction.`
      );
      return;
    }

    safety.reasons.push(
      `HIP-3 dex abstraction is not enabled for ${args.market.dex}. Re-run with enableDexAbstraction=true or enable dexAbstraction separately first.`
    );
    safety.approved = false;
    safety.decision = "reject";
  }

  private getDailyOrderNotionalUsed(): number {
    const today = new Date().toISOString().slice(0, 10);
    return readLogEvents()
      .filter((event) => event.timestamp.startsWith(today))
      .filter((event) => event.action === "place_hyperliquid_order")
      .filter((event) => ["success", "submitted"].includes(event.status))
      .filter((event) => event.details.reduceOnly !== true)
      .reduce((sum, event) => {
        const notionalUsd = Number(event.details.notionalUsd ?? 0);
        return Number.isFinite(notionalUsd) ? sum + notionalUsd : sum;
      }, 0);
  }

  private toSdkTimeInForce(timeInForce: HyperliquidTimeInForce | "ioc", orderType: "market" | "limit") {
    if (orderType === "market") {
      return "FrontendMarket" as const;
    }

    if (timeInForce === "alo") {
      return "Alo" as const;
    }

    if (timeInForce === "ioc") {
      return "Ioc" as const;
    }

    return "Gtc" as const;
  }
}
