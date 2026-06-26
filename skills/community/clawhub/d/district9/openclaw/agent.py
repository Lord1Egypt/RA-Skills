"""Agent main loop controller."""

import signal
import time

from .config import OpenClawConfig
from .sensing import SensorManager
from .brain.synthesizer import MemeSynthesizer
from .brain.evaluator import MemeEvaluator
from .creator.metadata import MetadataBuilder
from .creator.logo_gen import LogoGenerator
from .launcher.flap import FlapLauncher
from .launcher.district9 import District9Launcher
from .utils.logger import log


class Agent:
    """OpenClaw Agent — sense, think, create, launch."""

    def __init__(self, config: OpenClawConfig, dry_run: bool = False):
        self.config = config
        self.dry_run = dry_run
        self.daily_launches = 0
        self._running = False

        # Initialize modules
        self.sensors = SensorManager(config.strategy.sources)
        self.synthesizer = MemeSynthesizer(config.strategy)
        self.evaluator = MemeEvaluator(config.strategy)
        self.metadata_builder = MetadataBuilder(config.agent_name)

        if config.launch.auto_generate_logo:
            self.logo_gen = LogoGenerator(
                provider=config.strategy.llm.provider,
                api_key=config.strategy.llm.api_key,
                base_url=config.strategy.llm.base_url,
            )
        else:
            self.logo_gen = None

        if not dry_run:
            if config.launch.platform == "district9":
                self.launcher = District9Launcher(config)
            else:
                self.launcher = FlapLauncher(config)
        else:
            self.launcher = None

    def run(self):
        """Main agent loop."""
        self._running = True
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)

        chain = self.config.chain
        if self.config.testnet:
            chain += " (testnet)"

        log.info(f"Agent '{self.config.agent_name}' started on {chain}")
        log.info(f"Scanning every {self.config.scan_interval}s")
        log.info(f"Max {self.config.strategy.max_daily_launches} launches/day")
        log.info("Tax: 1% (0.5% DISTRICT9 + 0.5% Agent)")
        log.info(f"Agent profile: https://www.district9.club/agent/{self.launcher.account.address if self.launcher else 'N/A'}")

        if self.dry_run:
            log.info("DRY RUN mode — will not launch tokens")
            self._cycle()
            return

        while self._running:
            try:
                self._cycle()
            except Exception as e:
                log.error(f"Cycle error: {e}")

            if self._running:
                log.info(f"Sleeping {self.config.scan_interval}s until next cycle...")
                time.sleep(self.config.scan_interval)

    def _cycle(self):
        """One complete sense -> think -> act cycle."""
        if self.daily_launches >= self.config.strategy.max_daily_launches:
            log.info("Daily launch limit reached.")
            return

        # SENSE
        log.info("Scanning information sources...")
        signals = self.sensors.scan_all()

        if not signals:
            log.info("No actionable signals found.")
            return

        log.info("Top signals:")
        for s in signals[:5]:
            log.info(f"  {s.source}: {s.keyword} (score: {s.score:.0f})")

        # THINK
        log.info(f"Generating meme concepts from {len(signals)} signals...")
        concepts = self.synthesizer.generate(signals, count=3)

        if not concepts:
            log.info("LLM generated no concepts.")
            return

        for c in concepts:
            log.info(f"  Concept: {c.name} ({c.symbol}) — raw score: {c.score:.0f}")

        log.info("Evaluating concepts...")
        best = self.evaluator.select_best(concepts)

        if not best:
            log.info("No concept scored high enough.")
            return

        log.info(f"Selected: {best.name} ({best.symbol}) — score: {best.score:.0f}/100")

        if self.dry_run:
            log.info(f"DRY RUN — would launch: {best.name} ({best.symbol})")
            log.info(f"  Narrative: {best.narrative[:200]}")
            log.info(f"  Logo prompt: {best.logo_prompt[:200]}")
            return

        # CREATE
        logo_path = ""
        if self.logo_gen:
            log.info("Generating logo...")
            logo_path = self.logo_gen.generate(best.name, best.narrative, best.logo_prompt)

        metadata = self.metadata_builder.build(
            name=best.name,
            symbol=best.symbol,
            narrative=best.narrative,
            logo_url="",  # will be set during IPFS upload
        )

        # LAUNCH
        platform = self.config.launch.platform
        log.info(f"Launching {best.symbol} via {platform}...")
        result = self.launcher.launch(metadata, image_path=logo_path)

        log.info(f"Token launched!")
        log.info(f"  Contract: {result['contract_address']}")
        if "flap_url" in result:
            log.info(f"  Flap: {result['flap_url']}")
        log.info(f"  DISTRICT9: {result['d9_token_url']}")
        log.info(f"  Explorer: {result['explorer_tx']}")

        self.daily_launches += 1

    def _handle_shutdown(self, signum, frame):
        log.info("Shutting down...")
        self._running = False
