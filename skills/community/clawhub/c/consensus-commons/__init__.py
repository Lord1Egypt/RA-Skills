"""Consensus Commons — Multi-agent adversarial decision council with consensus hardening."""
from .models import Intent, Post, PostTree, LockState
from .client import MockSpacebaseClient
from .routing import IntentRouter, RouteDecision
from .council import CouncilRunner, CouncilReport
