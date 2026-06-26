#!/usr/bin/env python3
# Copyright (c) 2026 李卓伦 (Zhuolun Li) — MIT License
"""
ClawSwarm Consensus Engine v1.0

Multi-agent prediction consensus with:
- MAD outlier filtering
- Adaptive anchoring (adjusts to prediction dispersion)
- Bias correction (corrects systematic bias)
- Multi-method aggregation (weighted + median + trimmed mean)

Usage:
  echo '{"predictions":[...], "anchor_price":100.0}' | python3 consensus.py
  python3 consensus.py --file input.json

Input JSON:
  {
    "predictions": [
      {"price": 100.5, "confidence": 70, "weight": 1.2},
      {"price": 99.8, "confidence": 60},
      ...
    ],
    "anchor_price": 100.0,
    "max_deviation": 0.05,
    "bias": 0.0
  }

  - predictions: array of prediction objects (price required, confidence/weight optional)
  - anchor_price: current/reference price for anchoring (required)
  - max_deviation: max allowed deviation as fraction, default 0.15 (15%)
  - bias: known systematic bias to correct, default 0

Output JSON:
  {
    "status": "success",
    "final_price": 100.23,
    "median_price": 100.30,
    "confidence": 72,
    "bull_ratio": 0.55,
    "participant_count": 45,
    "filtered_count": 42,
    "logic": "v1 | f=42/45 | anchor=0.30 | dev=0.23%"
  }
"""

import numpy as np
import json
import sys
import argparse


class ConsensusEngine:
    """
    Multi-agent consensus engine.
    Takes N predictions, filters outliers, applies weighted aggregation,
    adaptive anchoring, and outputs a consensus prediction.
    """

    def __init__(self, predictions, anchor_price, max_deviation=0.15, bias=0.0):
        """
        Args:
            predictions: list of dicts with 'price', optional 'confidence' and 'weight'
            anchor_price: reference price for anchoring and clamping
            max_deviation: max allowed deviation from anchor as fraction (0.15 = 15%)
            bias: systematic bias to correct before aggregation
        """
        self.raw_predictions = predictions
        self.prices = np.array([p['price'] for p in predictions], dtype=np.float64)
        self.confidences = np.array([p.get('confidence', 50) for p in predictions], dtype=np.float64)
        self.weights = np.array([p.get('weight', 1.0) for p in predictions], dtype=np.float64)
        self.anchor = float(anchor_price)
        self.max_dev = float(max_deviation)
        self.bias = float(bias)

    def filter_outliers_mad(self, data):
        """MAD (Median Absolute Deviation) outlier filter. More robust than IQR."""
        if len(data) < 5:
            return data, np.arange(len(data))

        median = np.median(data)
        mad = np.median(np.abs(data - median))

        if mad == 0:
            return data, np.arange(len(data))

        modified_z = 0.6745 * (data - median) / mad
        mask = np.abs(modified_z) < 3.5
        filtered = data[mask]

        if len(filtered) < 3:
            return data, np.arange(len(data))

        return filtered, np.where(mask)[0]

    def filter_by_anchor(self, data):
        """Filter predictions too far from anchor price."""
        max_dist = self.anchor * self.max_dev
        mask = np.abs(data - self.anchor) <= max_dist
        filtered = data[mask]

        if len(filtered) < 3:
            return data, np.arange(len(data))

        return filtered, np.where(mask)[0]

    def bias_correct(self, data):
        """Subtract known systematic bias."""
        if self.bias != 0:
            return data - self.bias
        return data

    def weighted_aggregate(self, data, weights):
        """Weighted aggregation using confidence * weight."""
        if len(weights) != len(data):
            weights = np.ones(len(data))

        w = weights / weights.sum()
        return float(np.sum(data * w))

    def adaptive_anchor(self, raw_pred, data):
        """
        Adaptive anchoring: the more dispersed predictions are,
        the more we anchor to the reference price.
        """
        if len(data) >= 3:
            std_pct = float(np.std(data) / self.anchor) if self.anchor != 0 else 0.01
        else:
            std_pct = 0.01

        base_anchor = 0.25
        dispersion_bonus = min(0.35, std_pct * 500)
        anchor_w = min(0.85, base_anchor + dispersion_bonus)

        anchored = raw_pred * (1 - anchor_w) + self.anchor * anchor_w
        return anchored, anchor_w

    def clamp(self, pred):
        """Clamp to max deviation from anchor."""
        max_delta = self.anchor * self.max_dev
        return float(np.clip(pred, self.anchor - max_delta, self.anchor + max_delta))

    def fuse(self):
        """
        Core fusion pipeline:
        1. Bias correction
        2. MAD outlier filtering
        3. Anchor-distance filtering
        4. Multi-method aggregation (weighted 40% + median 35% + trimmed mean 25%)
        5. Adaptive anchoring
        6. Clamping
        """
        data = self.prices.copy()
        total = len(data)

        if total == 0:
            return {
                'status': 'error',
                'message': 'No predictions provided'
            }

        if total == 1:
            price = self.clamp(float(data[0]))
            return {
                'status': 'success',
                'final_price': round(price, 4),
                'median_price': round(price, 4),
                'confidence': int(self.confidences[0]),
                'bull_ratio': 1.0 if price >= self.anchor else 0.0,
                'participant_count': 1,
                'filtered_count': 1,
                'logic': 'v1 | single agent | no consensus needed'
            }

        # Step 1: Bias correction
        corrected = self.bias_correct(data)

        # Step 2: MAD outlier filtering
        filtered, mad_idx = self.filter_outliers_mad(corrected)
        kept_weights = self.weights[mad_idx] * (self.confidences[mad_idx] / 100.0)

        # Step 3: Anchor-distance filtering
        filtered, dist_idx = self.filter_by_anchor(filtered)
        kept_weights = kept_weights[dist_idx]

        # Step 4: Multi-method aggregation
        median_val = float(np.median(filtered))
        weighted_val = self.weighted_aggregate(filtered, kept_weights)

        if len(filtered) >= 5:
            n = max(1, int(len(filtered) * 0.15))
            s = np.sort(filtered)
            trimmed = s[n:-n] if len(s[n:-n]) > 0 else s
            trimmed_val = float(np.mean(trimmed))
        else:
            trimmed_val = float(np.mean(filtered))

        raw = weighted_val * 0.40 + median_val * 0.35 + trimmed_val * 0.25

        # Step 5: Adaptive anchoring
        anchored, anchor_w = self.adaptive_anchor(raw, filtered)

        # Step 6: Clamp
        final = self.clamp(anchored)

        # Confidence
        n_agents = len(filtered)
        std_pct = float(np.std(filtered) / np.mean(filtered) * 100) if len(filtered) > 1 else 10
        confidence = min(100, int(n_agents * 3 + max(0, 50 - std_pct * 50)))

        # Bull/bear ratio
        bull = int(np.sum(filtered >= median_val))
        bull_ratio = round(bull / len(filtered), 2)

        dev = abs(final - self.anchor) / self.anchor * 100 if self.anchor != 0 else 0

        return {
            'status': 'success',
            'final_price': round(final, 4),
            'median_price': round(median_val, 4),
            'confidence': confidence,
            'bull_ratio': bull_ratio,
            'bear_ratio': round(1 - bull_ratio, 2),
            'participant_count': total,
            'filtered_count': n_agents,
            'logic': f'v1 | f={n_agents}/{total} | bias={self.bias:.1f} | anchor={anchor_w:.2f} | dev={dev:.4f}%'
        }


def main():
    parser = argparse.ArgumentParser(description='ClawSwarm Consensus Engine')
    parser.add_argument('--file', '-f', help='Input JSON file (default: stdin)')
    args = parser.parse_args()

    try:
        if args.file:
            with open(args.file) as f:
                raw = f.read()
        else:
            raw = sys.stdin.read()

        if not raw.strip():
            print(json.dumps({'status': 'error', 'message': 'No input'}))
            sys.exit(1)

        d = json.loads(raw)

        engine = ConsensusEngine(
            predictions=d['predictions'],
            anchor_price=d['anchor_price'],
            max_deviation=d.get('max_deviation', 0.15),
            bias=d.get('bias', 0.0)
        )

        result = engine.fuse()
        print(json.dumps(result, indent=2))

    except KeyError as e:
        print(json.dumps({'status': 'error', 'message': f'Missing field: {e}'}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({'status': 'error', 'message': str(e)}))
        sys.exit(1)


if __name__ == '__main__':
    main()
