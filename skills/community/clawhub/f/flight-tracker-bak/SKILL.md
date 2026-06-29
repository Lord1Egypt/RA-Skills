---
name: flight-tracker
description: Busca automatizada de passagens aéreas MAO→CNF com cron 2x/dia e relatório no WhatsApp
---

# Flight Tracker — MAO → CNF

Busca passagens aéreas de Manaus (MAO) para Belo Horizonte/Confins (CNF) às 09:00 e 15:00 todos os dias.

## Critérios
- **Rota:** Manaus (MAO) → Belo Horizonte (CNF)
- **Tipo:** Somente ida
- **Período:** 7 a 14 de Agosto de 2026
- **Duração máx:** 7 horas
- **Conexões máx:** 1
- **Chegada:** Entre 8h e 16h
- **Preço máx:** R$ 1.000
- **Prioridade:** Azul > Latam (nesta ordem)
- **Saída:** Top 5 mais baratos

## Como funciona
1. Cron job às 09:00 e 15:00 (America/Manaus)
2. Executa script PowerShell que tenta múltiplas fontes
3. Relata resultados no WhatsApp

## Fontes testadas
- Google Flights
- ViajaNet
- SkyScanner
- LATAM

## Arquivos
- `scripts/search-flights.ps1` — Script de busca
- `search-flights.md` — Resultados da última execução
