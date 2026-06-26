"""All dataclasses for /depradar.

Canonical data model used throughout the processing pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ── Sub-scores (per-item scoring components) ─────────────────────────────────

@dataclass
class SubScores:
    severity:  int = 0   # 0-100  How breaking is this change?
    recency:   int = 0   # 0-100  How recent is the release?
    impact:    int = 0   # 0-100  How many of YOUR files are affected?
    community: int = 0   # 0-100  How much community pain evidence?

    def to_dict(self) -> Dict[str, int]:
        return {
            "severity":  self.severity,
            "recency":   self.recency,
            "impact":    self.impact,
            "community": self.community,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "SubScores":
        return cls(
            severity  = d.get("severity", 0),
            recency   = d.get("recency", 0),
            impact    = d.get("impact", 0),
            community = d.get("community", 0),
        )


# ── Impact location in the user's codebase ───────────────────────────────────

@dataclass
class ImpactLocation:
    file_path:        str           # "src/payments/webhook.ts"
    line_number:      int           # 47
    usage_text:       str           # full code line (stripped)
    detection_method: str = "grep"  # "ast" | "grep"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "file_path":        self.file_path,
            "line_number":      self.line_number,
            "usage_text":       self.usage_text,
            "detection_method": self.detection_method,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ImpactLocation":
        return cls(
            file_path        = d["file_path"],
            line_number      = d["line_number"],
            usage_text       = d["usage_text"],
            detection_method = d.get("detection_method", "grep"),
        )


# ── A single breaking change detected in a release ───────────────────────────

@dataclass
class BreakingChange:
    symbol:        str            # "stripe.webhooks.constructEvent"
    change_type:   str            # "removed"|"renamed"|"signature_changed"|
                                  # "behavior_changed"|"deprecated"|"type_changed"|"other"
    description:   str            # Human-readable summary
    old_signature: Optional[str] = None  # Before the change
    new_signature: Optional[str] = None  # After the change  (None if removed)
    migration_note: Optional[str] = None # What to do
    source:        str = "release_notes" # "release_notes"|"changelog"|"commit"
    confidence:    str = "med"           # "high"|"med"|"low"
    source_excerpt: Optional[str] = None # Exact line/sentence from changelog that triggered this

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol":         self.symbol,
            "change_type":    self.change_type,
            "description":    self.description,
            "old_signature":  self.old_signature,
            "new_signature":  self.new_signature,
            "migration_note": self.migration_note,
            "source":         self.source,
            "confidence":     self.confidence,
            "source_excerpt": self.source_excerpt,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "BreakingChange":
        return cls(
            symbol         = d["symbol"],
            change_type    = d["change_type"],
            description    = d["description"],
            old_signature  = d.get("old_signature"),
            new_signature  = d.get("new_signature"),
            migration_note = d.get("migration_note"),
            source         = d.get("source", "release_notes"),
            confidence     = d.get("confidence", "med"),
            source_excerpt = d.get("source_excerpt"),
        )


# ── Per-package update result ─────────────────────────────────────────────────

@dataclass
class PackageUpdate:
    id:              str           # "P1", "P2", …
    package:         str           # "stripe"
    ecosystem:       str           # "npm"|"pypi"|"cargo"|"maven"|"gem"|"go"
    current_version: str           # "7.0.0"  (what your project declares)
    latest_version:  str           # "8.2.0"  (newest stable)
    semver_type:     str           # "major"|"minor"|"patch"|"none"|"unknown"
    has_breaking_changes: bool = False
    breaking_changes: List[BreakingChange] = field(default_factory=list)
    changelog_url:   Optional[str] = None
    release_date:    Optional[str] = None   # "2026-01-15"
    release_notes_snippet: Optional[str] = None  # First ~400 chars
    impact_locations: List[ImpactLocation] = field(default_factory=list)
    impact_confidence: str = "not_scanned"  # "high"|"med"|"low"|"not_scanned"
    github_repo:     Optional[str] = None   # "stripe/stripe-node"
    subs:            Optional[SubScores] = None
    score:           int = 0
    cross_refs:      List[str] = field(default_factory=list)
    semver_violation: bool = False          # True if breaking change detected in minor/patch release
    workspace_versions: Dict[str, str] = field(default_factory=dict)  # {source_file_path: version}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id":              self.id,
            "package":         self.package,
            "ecosystem":       self.ecosystem,
            "current_version": self.current_version,
            "latest_version":  self.latest_version,
            "semver_type":     self.semver_type,
            "has_breaking_changes": self.has_breaking_changes,
            "breaking_changes": [bc.to_dict() for bc in self.breaking_changes],
            "changelog_url":   self.changelog_url,
            "release_date":    self.release_date,
            "release_notes_snippet": self.release_notes_snippet,
            "impact_locations": [loc.to_dict() for loc in self.impact_locations],
            "impact_confidence": self.impact_confidence,
            "github_repo":     self.github_repo,
            "subs":            self.subs.to_dict() if self.subs else None,
            "score":           self.score,
            "cross_refs":      self.cross_refs,
            "semver_violation": self.semver_violation,
            "workspace_versions": self.workspace_versions,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "PackageUpdate":
        return cls(
            id              = d["id"],
            package         = d["package"],
            ecosystem       = d["ecosystem"],
            current_version = d["current_version"],
            latest_version  = d["latest_version"],
            semver_type     = d["semver_type"],
            has_breaking_changes = d.get("has_breaking_changes", False),
            breaking_changes = [BreakingChange.from_dict(x)
                                 for x in d.get("breaking_changes", [])],
            changelog_url    = d.get("changelog_url"),
            release_date     = d.get("release_date"),
            release_notes_snippet = d.get("release_notes_snippet"),
            impact_locations = [ImpactLocation.from_dict(x)
                                 for x in d.get("impact_locations", [])],
            impact_confidence = d.get("impact_confidence", "not_scanned"),
            github_repo      = d.get("github_repo"),
            subs             = SubScores.from_dict(d["subs"]) if d.get("subs") else None,
            score            = d.get("score", 0),
            cross_refs       = d.get("cross_refs", []),
            semver_violation = d.get("semver_violation", False),
            workspace_versions = d.get("workspace_versions", {}),
        )


# ── Community signal items ────────────────────────────────────────────────────

@dataclass
class GithubIssueItem:
    id:               str          # "GI1", "GI2", …
    package:          str
    version:          str
    title:            str
    url:              str
    body_snippet:     Optional[str] = None
    comments:         int = 0
    labels:           List[str] = field(default_factory=list)
    state:            str = "open"  # "open"|"closed"
    resolution_snippet: Optional[str] = None
    created_at:       Optional[str] = None
    subs:             Optional[SubScores] = None
    score:            int = 0
    cross_refs:       List[str] = field(default_factory=list)
    has_accepted_answer: bool = False   # True if issue has a linked/accepted resolution
    quality_weight:   float = 1.0       # Multiplier: closed+answered=2.0, open+no comments=0.8

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id":                 self.id,
            "package":            self.package,
            "version":            self.version,
            "title":              self.title,
            "url":                self.url,
            "body_snippet":       self.body_snippet,
            "comments":           self.comments,
            "labels":             self.labels,
            "state":              self.state,
            "resolution_snippet": self.resolution_snippet,
            "created_at":         self.created_at,
            "subs":               self.subs.to_dict() if self.subs else None,
            "score":              self.score,
            "cross_refs":         self.cross_refs,
            "has_accepted_answer": self.has_accepted_answer,
            "quality_weight":     self.quality_weight,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "GithubIssueItem":
        return cls(
            id                 = d["id"],
            package            = d["package"],
            version            = d.get("version", ""),
            title              = d["title"],
            url                = d["url"],
            body_snippet       = d.get("body_snippet"),
            comments           = d.get("comments", 0),
            labels             = d.get("labels", []),
            state              = d.get("state", "open"),
            resolution_snippet = d.get("resolution_snippet"),
            created_at         = d.get("created_at"),
            subs               = SubScores.from_dict(d["subs"]) if d.get("subs") else None,
            score              = d.get("score", 0),
            cross_refs         = d.get("cross_refs", []),
            has_accepted_answer = d.get("has_accepted_answer", False),
            quality_weight     = d.get("quality_weight", 1.0),
        )


@dataclass
class StackOverflowItem:
    id:                    str   # "SO1", …
    package:               str
    question_title:        str
    question_url:          str
    answer_count:          int = 0
    is_answered:           bool = False
    accepted_answer_snippet: Optional[str] = None
    tags:                  List[str] = field(default_factory=list)
    view_count:            int = 0
    so_score:              int = 0   # vote score
    created_at:            Optional[str] = None
    subs:                  Optional[SubScores] = None
    score:                 int = 0
    cross_refs:            List[str] = field(default_factory=list)
    quality_weight:        float = 1.0  # Multiplier: answered+accepted=2.0, unanswered=0.8

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id":                      self.id,
            "package":                 self.package,
            "question_title":          self.question_title,
            "question_url":            self.question_url,
            "answer_count":            self.answer_count,
            "is_answered":             self.is_answered,
            "accepted_answer_snippet": self.accepted_answer_snippet,
            "tags":                    self.tags,
            "view_count":              self.view_count,
            "so_score":                self.so_score,
            "created_at":              self.created_at,
            "subs":                    self.subs.to_dict() if self.subs else None,
            "score":                   self.score,
            "cross_refs":              self.cross_refs,
            "quality_weight":          self.quality_weight,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "StackOverflowItem":
        return cls(
            id                      = d["id"],
            package                 = d["package"],
            question_title          = d["question_title"],
            question_url            = d["question_url"],
            answer_count            = d.get("answer_count", 0),
            is_answered             = d.get("is_answered", False),
            accepted_answer_snippet = d.get("accepted_answer_snippet"),
            tags                    = d.get("tags", []),
            view_count              = d.get("view_count", 0),
            so_score                = d.get("so_score", 0),
            created_at              = d.get("created_at"),
            subs                    = SubScores.from_dict(d["subs"]) if d.get("subs") else None,
            score                   = d.get("score", 0),
            cross_refs              = d.get("cross_refs", []),
            quality_weight          = d.get("quality_weight", 1.0),
        )


@dataclass
class RedditItem:
    id:           str    # "RI1", …
    package:      str
    subreddit:    str
    title:        str
    url:          str
    reddit_score: int = 0
    num_comments: int = 0
    top_comment:  Optional[str] = None
    date:         Optional[str] = None
    date_confidence: str = "low"
    subs:         Optional[SubScores] = None
    score:        int = 0
    cross_refs:   List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id":           self.id,
            "package":      self.package,
            "subreddit":    self.subreddit,
            "title":        self.title,
            "url":          self.url,
            "reddit_score": self.reddit_score,
            "num_comments": self.num_comments,
            "top_comment":  self.top_comment,
            "date":         self.date,
            "date_confidence": self.date_confidence,
            "subs":         self.subs.to_dict() if self.subs else None,
            "score":        self.score,
            "cross_refs":   self.cross_refs,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "RedditItem":
        return cls(
            id             = d["id"],
            package        = d["package"],
            subreddit      = d["subreddit"],
            title          = d["title"],
            url            = d["url"],
            reddit_score   = d.get("reddit_score", 0),
            num_comments   = d.get("num_comments", 0),
            top_comment    = d.get("top_comment"),
            date           = d.get("date"),
            date_confidence = d.get("date_confidence", "low"),
            subs           = SubScores.from_dict(d["subs"]) if d.get("subs") else None,
            score          = d.get("score", 0),
            cross_refs     = d.get("cross_refs", []),
        )


@dataclass
class HackerNewsItem:
    id:          str    # "HN1", …
    package:     str
    title:       str
    url:         Optional[str]
    hn_url:      str
    points:      int = 0
    num_comments: int = 0
    top_comment: Optional[str] = None
    date:        Optional[str] = None
    date_confidence: str = "high"
    subs:        Optional[SubScores] = None
    score:       int = 0
    cross_refs:  List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id":           self.id,
            "package":      self.package,
            "title":        self.title,
            "url":          self.url,
            "hn_url":       self.hn_url,
            "points":       self.points,
            "num_comments": self.num_comments,
            "top_comment":  self.top_comment,
            "date":         self.date,
            "date_confidence": self.date_confidence,
            "subs":         self.subs.to_dict() if self.subs else None,
            "score":        self.score,
            "cross_refs":   self.cross_refs,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "HackerNewsItem":
        return cls(
            id             = d["id"],
            package        = d["package"],
            title          = d["title"],
            url            = d.get("url"),
            hn_url         = d["hn_url"],
            points         = d.get("points", 0),
            num_comments   = d.get("num_comments", 0),
            top_comment    = d.get("top_comment"),
            date           = d.get("date"),
            date_confidence = d.get("date_confidence", "high"),
            subs           = SubScores.from_dict(d["subs"]) if d.get("subs") else None,
            score          = d.get("score", 0),
            cross_refs     = d.get("cross_refs", []),
        )


@dataclass
class TwitterItem:
    id:           str   # "TW1", …
    package:      str
    text:         str
    author_handle: str
    likes:        int = 0
    reposts:      int = 0
    replies:      int = 0
    date:         Optional[str] = None
    url:          Optional[str] = None
    subs:         Optional[SubScores] = None
    score:        int = 0
    cross_refs:   List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id":           self.id,
            "package":      self.package,
            "text":         self.text,
            "author_handle": self.author_handle,
            "likes":        self.likes,
            "reposts":      self.reposts,
            "replies":      self.replies,
            "date":         self.date,
            "url":          self.url,
            "subs":         self.subs.to_dict() if self.subs else None,
            "score":        self.score,
            "cross_refs":   self.cross_refs,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TwitterItem":
        return cls(
            id            = d["id"],
            package       = d["package"],
            text          = d["text"],
            author_handle = d["author_handle"],
            likes         = d.get("likes", 0),
            reposts       = d.get("reposts", 0),
            replies       = d.get("replies", 0),
            date          = d.get("date"),
            url           = d.get("url"),
            subs          = SubScores.from_dict(d["subs"]) if d.get("subs") else None,
            score         = d.get("score", 0),
            cross_refs    = d.get("cross_refs", []),
        )


# ── Dependency info (from manifest parsing) ───────────────────────────────────

@dataclass
class DepInfo:
    name:        str
    version_spec: str       # Raw spec: "^7.0.0", ">=1.0,<2", "7.0.0"
    version:     str        # Resolved numeric: "7.0.0"
    ecosystem:   str        # "npm"|"pypi"|"cargo"|"maven"|"gem"|"go"
    source_file: str        # "package.json", "requirements.txt"
    is_dev:      bool = False
    github_repo: Optional[str] = None   # "stripe/stripe-node" if resolved
    workspace_versions: Dict[str, str] = field(default_factory=dict)  # {abs_path: version}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name":               self.name,
            "version_spec":       self.version_spec,
            "version":            self.version,
            "ecosystem":          self.ecosystem,
            "source_file":        self.source_file,
            "is_dev":             self.is_dev,
            "github_repo":        self.github_repo,
            "workspace_versions": self.workspace_versions,
        }


# ── Top-level report ──────────────────────────────────────────────────────────

@dataclass
class DepRadarReport:
    project_path:   str
    dep_files_found: List[str]

    packages_scanned: int = 0
    packages_with_breaking_changes: List[PackageUpdate] = field(default_factory=list)
    packages_with_minor_updates:    List[PackageUpdate] = field(default_factory=list)
    packages_current:  List[str] = field(default_factory=list)
    packages_not_found: List[str] = field(default_factory=list)

    # Community signals
    github_issues: List[GithubIssueItem] = field(default_factory=list)
    stackoverflow: List[StackOverflowItem] = field(default_factory=list)
    reddit:        List[RedditItem] = field(default_factory=list)
    hackernews:    List[HackerNewsItem] = field(default_factory=list)
    twitter:       List[TwitterItem] = field(default_factory=list)

    # Error tracking
    registry_errors:       Dict[str, str] = field(default_factory=dict)
    registry_fetch_errors: Dict[str, str] = field(default_factory=dict)  # transient: timeout/network (distinct from 404)
    community_errors:      Dict[str, str] = field(default_factory=dict)
    scan_errors:           Dict[str, str] = field(default_factory=dict)
    dep_parse_errors:      List[str] = field(default_factory=list)        # Parse errors from dep files
    rate_limit_hits:       Dict[str, int] = field(default_factory=dict)   # {source: count}
    rate_limited_packages: List[str] = field(default_factory=list)        # Packages skipped due to rate limit
    scan_skipped:          List[str] = field(default_factory=list)        # Files skipped in scan

    # Partial results flag — True when any packages could not be checked
    partial_results: bool = False

    # Cache metadata
    from_cache:     bool = False
    cache_age_hours: Optional[float] = None

    # Run metadata
    depth:          str = "default"
    days_window:    int = 30
    generated_at:   str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_path":    self.project_path,
            "dep_files_found": self.dep_files_found,
            "packages_scanned": self.packages_scanned,
            "packages_with_breaking_changes": [p.to_dict() for p in self.packages_with_breaking_changes],
            "packages_with_minor_updates":    [p.to_dict() for p in self.packages_with_minor_updates],
            "packages_current":   self.packages_current,
            "packages_not_found": self.packages_not_found,
            "github_issues": [x.to_dict() for x in self.github_issues],
            "stackoverflow":  [x.to_dict() for x in self.stackoverflow],
            "reddit":         [x.to_dict() for x in self.reddit],
            "hackernews":     [x.to_dict() for x in self.hackernews],
            "twitter":        [x.to_dict() for x in self.twitter],
            "registry_errors":       self.registry_errors,
            "registry_fetch_errors": self.registry_fetch_errors,
            "community_errors":      self.community_errors,
            "scan_errors":           self.scan_errors,
            "dep_parse_errors":      self.dep_parse_errors,
            "rate_limit_hits":       self.rate_limit_hits,
            "rate_limited_packages": self.rate_limited_packages,
            "scan_skipped":          self.scan_skipped,
            "partial_results":       self.partial_results,
            "from_cache":      self.from_cache,
            "cache_age_hours": self.cache_age_hours,
            "depth":           self.depth,
            "days_window":     self.days_window,
            "generated_at":    self.generated_at,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "DepRadarReport":
        return cls(
            project_path    = d.get("project_path", ""),
            dep_files_found = d.get("dep_files_found", []),
            packages_scanned = d.get("packages_scanned", 0),
            packages_with_breaking_changes = [
                PackageUpdate.from_dict(x)
                for x in d.get("packages_with_breaking_changes", [])
            ],
            packages_with_minor_updates = [
                PackageUpdate.from_dict(x)
                for x in d.get("packages_with_minor_updates", [])
            ],
            packages_current   = d.get("packages_current", []),
            packages_not_found = d.get("packages_not_found", []),
            github_issues = [GithubIssueItem.from_dict(x) for x in d.get("github_issues", [])],
            stackoverflow  = [StackOverflowItem.from_dict(x) for x in d.get("stackoverflow", [])],
            reddit         = [RedditItem.from_dict(x) for x in d.get("reddit", [])],
            hackernews     = [HackerNewsItem.from_dict(x) for x in d.get("hackernews", [])],
            twitter        = [TwitterItem.from_dict(x) for x in d.get("twitter", [])],
            registry_errors       = d.get("registry_errors", {}),
            registry_fetch_errors = d.get("registry_fetch_errors", {}),
            community_errors      = d.get("community_errors", {}),
            scan_errors           = d.get("scan_errors", {}),
            dep_parse_errors      = d.get("dep_parse_errors", []),
            rate_limit_hits       = d.get("rate_limit_hits", {}),
            rate_limited_packages = d.get("rate_limited_packages", []),
            scan_skipped          = d.get("scan_skipped", []),
            partial_results       = d.get("partial_results", False),
            from_cache       = d.get("from_cache", False),
            cache_age_hours  = d.get("cache_age_hours"),
            depth            = d.get("depth", "default"),
            days_window      = d.get("days_window", 30),
            generated_at     = d.get("generated_at", ""),
        )
