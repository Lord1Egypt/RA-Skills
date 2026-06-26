# Skill: finance-trading

_La stratégie quantitative pour le paper trading BTC/USDT_

## 1. Analyse Technique (1h et 15min)

**Indicateurs :**
- EMA 20 (Moyenne Mobile Exponentielle 20 périodes)
- EMA 50 (Moyenne Mobile Exponentielle 50 périodes)
- RSI (Relative Strength Index)

**Signal d'Achat :**
- EMA 20 > EMA 50 (crossing haussier)
- RSI entre 40 et 60 (momentum haussier)

**Signal de Vente :**
- EMA 20 < EMA 50 (crossing baissier)
- RSI > 80 (surachat)

## 2. Gestion de Risque

- **Mode :** PAPER TRADING uniquement
- **Taille maximum :** 5% du capital fictif par trade
- **Stop Loss :** 2%
- **Take Profit :** 6%

## 3. Rapport & Suivi

- **Journal :** `trading_log.md` après chaque trade
- **Rapport quotidien :** Chaque jour à 18h → rapport de performance avec solde, PnL, Win Rate, sentiment marché

## 4. Fréquence

- **Vérification :** Toutes les 15 minutes
- **Veille :** Le reste du temps

---

**Exécution :**
```bash
# Analyser le marché
fetch market-data BTC/USDT --timeframes 1h 15min

# Calculer les indicateurs
calculate-indicators --ema-20 --ema-50 --rsi

# Appliquer la stratégie
apply-strategy --mode paper --risk 5% --sl 2% --tp 6%

# Journaliser
log-trade --file trading_log.md
```
