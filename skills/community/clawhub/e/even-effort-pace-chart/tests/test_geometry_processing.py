import math
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import pace_chart as pace


def route(samples):
    factor = 180 / (math.pi * 6371008.8)
    return pace.Route([(0, x * factor, z) for x, z in samples],
                      [pace.Sample(x, z) for x, z in samples], [])


def totals(profile):
    return (sum(max(0, b.elevation_m - a.elevation_m) for a, b in zip(profile, profile[1:])),
            sum(max(0, a.elevation_m - b.elevation_m) for a, b in zip(profile, profile[1:])))


class ProfileProcessingTests(unittest.TestCase):
    def test_smoothing_preserves_linear_climbs_and_endpoints(self):
        for length in (20, 100, 1000):
            for slope in (-0.2, 0.2):
                source = route([(0, 10), (length, 10 + length * slope)])
                result = pace.smooth_profile(source, 5, 100)
                for sample in result:
                    self.assertAlmostEqual(sample.elevation_m, 10 + sample.distance_m * slope)

    def test_window_integrates_original_vertices_between_grid_points(self):
        source = route([(0, 0), (11, 0), (12, 10), (13, 0), (30, 0)])
        result = pace.smooth_profile(source, 5, 20)
        self.assertAlmostEqual(result[3].elevation_m, 0.5)

    def test_default_hysteresis_uses_source_peaks_and_ten_metre_threshold(self):
        for height, expected in ((9, 0), (10, 10), (12, 12)):
            with self.subTest(height=height):
                source = route([(0, 0), (11, 0), (12, height), (13, 0), (30, 0)])
                result = pace.ascent_profile(source)
                self.assertEqual(totals(result), (expected, expected))
                self.assertEqual([p.distance_m for p in result],
                                 [p.distance_m for p in source.samples])

    def test_hysteresis_preserves_short_hills_at_different_sampling_densities(self):
        for spacing in (1, 2, 5, 10):
            source = route([(x, max(0, 20 * (1 - abs(x - 150) / 50)))
                            for x in range(0, 301, spacing)])
            result = pace.ascent_profile(source, 5, 0, "hysteresis", 3)
            self.assertEqual(totals(result), (20, 20))

    def test_hysteresis_accumulates_gentle_ramps_and_suppresses_small_reversals(self):
        source = route([(x, x / 100 + (0.4 if x % 20 else 0))
                        for x in range(0, 1001, 10)])
        result = pace.ascent_profile(source, 5, 0, "hysteresis", 3)
        # Interior reversals vanish; the terminal peak and endpoint retain the final 0.3 m descent.
        self.assertAlmostEqual(totals(result)[0], 10.3)
        self.assertAlmostEqual(totals(result)[1], 0.3)
        self.assertEqual((result[0], result[-1]), (source.samples[0], source.samples[-1]))

    def test_peak_valley_threshold_preserves_plateaus_and_cp_additivity(self):
        source = route([(0, 0), (100, 0), (110, 20), (150, 20),
                        (160, 0), (200, 0), (250, 10), (300, 0)])
        profile = pace.ascent_profile(source, 5, 0, "hysteresis", 3)
        self.assertEqual(totals(profile), (30, 30))
        parts = [pace.section_stats(profile, a, b, 1, 700, profile)
                 for a, b in zip((0, 105, 130, 170), (105, 130, 170, 300))]
        self.assertEqual(sum(p["ascent_m"] for p in parts), 30)
        self.assertEqual(sum(p["descent_m"] for p in parts), 30)
        self.assertEqual(pace.interpolate(profile, 100), 0)

    def test_zero_threshold_and_window_method_are_explicit_options(self):
        source = route([(0, 0), (10, 1), (20, 0), (30, 10), (40, 0)])
        self.assertEqual(totals(pace.ascent_profile(source, 5, 0, "hysteresis", 0)), (11, 11))
        self.assertEqual(pace.ascent_profile(source, 5, 20, "window", 3),
                         pace.smooth_profile(source, 5, 20))
        with self.assertRaises(pace.InputError):
            pace.ascent_profile(source, 5, 0, "unknown", 3)

    def test_confirmed_extrema_near_endpoints_are_retained(self):
        for heights in ([0, -2, 2, 0], [0, 2, -2, 0]):
            source = route([(i * 100, z) for i, z in enumerate(heights)])
            result = pace.ascent_profile(source, 5, 0, "hysteresis", 3)
            self.assertEqual(totals(result), (4, 4))

    def test_tiny_final_interval_does_not_create_elevation(self):
        for remainder in (1e-12, 1e-10, 1e-8, 0.01):
            source = route([(0, 1000), (1000 + remainder, 1000)])
            result = pace.smooth_profile(source, 5, 20)
            for sample in result:
                self.assertAlmostEqual(sample.elevation_m, 1000, places=8)
            self.assertAlmostEqual(totals(result)[0], 0, places=8)


class InputQualityTests(unittest.TestCase):
    def test_isolated_positive_and_negative_spikes_are_corrected_and_reported(self):
        for spike in (-100, 100):
            source = route([(x, spike if x == 50 else 0) for x in range(0, 101, 5)])
            processed = pace.prepare_route(source, 0, 30)
            self.assertEqual(totals(processed.samples), (0, 0))
            self.assertEqual(processed.diagnostics["elevation_spikes_corrected"], 1)
            self.assertTrue(processed.warnings)
            self.assertEqual(source.samples[10].elevation_m, spike)
            disabled = pace.prepare_route(source, 0, 0)
            self.assertEqual(disabled.samples, source.samples)

    def test_real_steep_hill_and_sustained_step_survive_spike_filter(self):
        for samples in (
            [(0, 0), (10, 20), (20, 0)],
            [(0, 0), (50, 100), (100, 0)],
            [(0, 0), (5, 0), (10, 100), (15, 100), (20, 100)],
        ):
            source = route(samples)
            processed = pace.prepare_route(source, 0, 30)
            self.assertEqual(processed.samples, source.samples)
            self.assertEqual(processed.diagnostics["elevation_spikes_corrected"], 0)

    def test_distance_filter_is_opt_in_reports_impact_and_preserves_elevation(self):
        factor = 180 / (math.pi * 6371008.8)
        points = [((2 if i % 2 else -2) * factor, i * 5 * factor, i / 10)
                  for i in range(201)]
        distances = [0]
        for a, b in zip(points, points[1:]):
            distances.append(distances[-1] + pace.haversine(a, b))
        source = pace.Route(points, [pace.Sample(x, p[2]) for x, p in zip(distances, points)], [])
        untouched = pace.prepare_route(source, 0, 30)
        self.assertAlmostEqual(untouched.total_m, 1280.624847, places=4)
        self.assertTrue(any("distance" in warning.lower() for warning in untouched.warnings))
        filtered = pace.prepare_route(source, 4.1, 30)
        self.assertAlmostEqual(filtered.total_m, 1000, delta=1)
        self.assertEqual(filtered.points[0], source.points[0])
        self.assertEqual(filtered.points[-1], source.points[-1])
        self.assertEqual([s.elevation_m for s in filtered.samples], [p[2] for p in points])
        self.assertGreater(filtered.diagnostics["distance_removed_m"], 270)
        self.assertEqual(totals(filtered.samples), (20, 0))

    def test_distance_filter_preserves_switchbacks_and_closed_loops(self):
        factor = 180 / (math.pi * 6371008.8)
        for xy in (
            [(0, 0), (50, 0), (0, 0)],
            [(0, 0), (100, 0), (0, 0), (100, 0)],
            [(0, 0), (50, 0), (50, 50), (0, 50), (0, 0)],
            [(0, 0), (50, 0), (50, 10), (0, 10)],
        ):
            points = [(y * factor, x * factor, 0) for x, y in xy]
            samples = [pace.Sample(0, 0)]
            for a, b in zip(points, points[1:]):
                samples.append(pace.Sample(samples[-1].distance_m + pace.haversine(a, b), 0))
            source = pace.Route(points, samples, [])
            processed = pace.prepare_route(source, 2, 30)
            self.assertAlmostEqual(processed.total_m, source.total_m, places=5)

    def test_simplification_keeps_elevation_at_its_spatial_checkpoint(self):
        factor = 180 / (math.pi * 6371008.8)
        points = [((2 if x % 2 else 0) * factor, x * factor, 10 if x == 100 else 0)
                  for x in range(101)] + [(0, 200 * factor, 0)]
        samples = [pace.Sample(0, 0)]
        for a, b in zip(points, points[1:]):
            samples.append(pace.Sample(samples[-1].distance_m + pace.haversine(a, b), b[2]))
        source = pace.Route(points, samples, [])
        processed = pace.prepare_route(source, 2.1, 0)
        self.assertAlmostEqual(processed.samples[100].distance_m, 100, places=5)
        cp = pace.projection_options(processed, {"lat": 0, "lon": 100 * factor})[0]["distance_m"]
        profile = pace.ascent_profile(processed, 5, 0, "hysteresis", 3)
        incoming = pace.section_stats(profile, 0, cp, 1, 700, profile)
        self.assertAlmostEqual(incoming["ascent_m"], 10, places=5)


if __name__ == "__main__":
    unittest.main()
