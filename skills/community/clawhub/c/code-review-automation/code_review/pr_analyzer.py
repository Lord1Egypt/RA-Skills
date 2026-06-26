"""Pull request analysis using Claude LLM."""

import time
from typing import List, Dict, Any

from github import PullRequest
from anthropic import APIError as AnthropicAPIError, RateLimitError

from .claude_client import ClaudeConfig
from .exceptions import APIError, AnalysisTimeoutError, DiffSizeError, EmptyDiffError
from .logger import setup_logger, log_exception, log_analysis_start, log_analysis_complete

logger = setup_logger(__name__)


class PRAnalyzer:
    """Analyze pull requests using Claude AI."""

    def __init__(self, timeout: int = 60, max_diff_size: int = 100000):
        """
        Initialize PR analyzer.

        Args:
            timeout: Analysis timeout in seconds
            max_diff_size: Maximum diff size in bytes
        """
        config = ClaudeConfig()
        self.client = config.get_client()
        self.model = "claude-3-7-sonnet-20250219"
        self.timeout = timeout
        self.max_diff_size = max_diff_size

    def analyze_pr(self, pr: PullRequest, diff_content: str) -> Dict[str, Any]:
        """Analyze a pull request using Claude.

        Args:
            pr: PullRequest object
            diff_content: Diff content as string

        Returns:
            Dictionary with analysis results

        Raises:
            EmptyDiffError: If diff is empty
            DiffSizeError: If diff size exceeds limit
            APIError: If Claude API call fails
        """
        # Validate diff content
        if not diff_content or diff_content.strip() == "":
            logger.warning(f"Empty diff for PR #{pr.number}")
            raise EmptyDiffError(pr.number)

        if len(diff_content) > self.max_diff_size:
            logger.error(f"Diff size {len(diff_content)} exceeds limit {self.max_diff_size}")
            raise DiffSizeError(len(diff_content), self.max_diff_size)

        # Log analysis start
        repo_name = f"{pr.base.repo.owner.login}/{pr.base.repo.name}"
        log_analysis_start(logger, repo_name, pr.number)

        start_time = time.time()

        try:
            # Build context from PR
            context = self._build_pr_context(pr, diff_content)

            # Create analysis prompt
            prompt = self._create_analysis_prompt(context)

            # Call Claude API
            logger.debug(f"Calling Claude API with model {self.model}")
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                timeout=self.timeout,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Parse response
            analysis_text = response.content[0].text

            # Calculate quality score
            quality_score = self.get_code_quality_score(analysis_text)

            duration = time.time() - start_time
            log_analysis_complete(logger, repo_name, pr.number, duration, 0)

            return {
                "pr_number": pr.number,
                "analysis": analysis_text,
                "model": self.model,
                "quality_score": quality_score
            }

        except AnthropicAPIError as e:
            duration = time.time() - start_time
            logger.error(f"Anthropic API error: {e}")
            raise APIError(
                f"Failed to analyze PR: {e}",
                status_code=getattr(e, 'status_code', None),
                suggestion="Check your API quota and network connection"
            )

        except RateLimitError as e:
            logger.error(f"Anthropic API rate limit exceeded: {e}")
            raise APIError(
                "Anthropic API rate limit exceeded",
                suggestion="Wait for rate limit to reset or check your usage limits"
            )

        except Exception as e:
            log_exception(logger, e, f"Failed to analyze PR #{pr.number}")
            raise APIError(
                f"Failed to analyze PR: {e}",
                suggestion="Check the error logs for more details"
            )

    def _build_pr_context(self, pr: PullRequest, diff_content: str) -> str:
        """Build context string from PR information.

        Args:
            pr: PullRequest object
            diff_content: Diff content as string

        Returns:
            Context string
        """
        # Get file changes
        files_info = []
        for file in pr.get_files():
            files_info.append(
                f"- {file.filename} ({file.status}): "
                f"+{file.additions}/-{file.deletions}"
            )

        files_str = "\n".join(files_info)

        context = f"""
# Pull Request Context

**PR Title:** {pr.title}
**PR Description:**
{pr.body or "No description provided"}

**Author:** {pr.user.login}
**State:** {pr.state}

## Files Changed
{files_str}

## Code Diff
{diff_content[:10000]}  # Limit to 10k chars to avoid token limits
"""

        return context

    def _create_analysis_prompt(self, context: str) -> str:
        """Create analysis prompt for Claude.

        Args:
            context: PR context string

        Returns:
            Analysis prompt
        """
        prompt = f"""You are an expert code reviewer. Analyze the following pull request and provide a comprehensive code review.

{context}

## Your Task

Provide a structured code review with the following sections:

### 1. Overall Assessment
- Brief summary of the PR's purpose
- General impression (positive/negative/mixed)
- Is the PR ready to merge?

### 2. Code Quality Issues
- Identify any bugs or potential bugs
- Logic errors
- Performance concerns
- Code style issues

### 3. Security Considerations
- Any security vulnerabilities
- Sensitive data handling
- Authentication/authorization issues

### 4. Best Practices
- Missing error handling
- Code organization
- Naming conventions
- Documentation

### 5. Recommendations
- Specific improvements with line-by-line suggestions where appropriate
- Priority levels (Critical, High, Medium, Low)

Format your response in markdown with clear headings. Be specific and actionable."""

        return prompt

    def get_code_quality_score(self, analysis_text: str) -> int:
        """Extract code quality score from analysis.

        Args:
            analysis_text: Analysis text from Claude

        Returns:
            Quality score (0-100)
        """
        # This is a simple heuristic. Could be enhanced with more sophisticated parsing.
        analysis_lower = analysis_text.lower()

        critical_count = analysis_lower.count("critical")
        high_count = analysis_lower.count("high priority")
        medium_count = analysis_lower.count("medium priority")

        # Start with 100 and deduct points based on issues
        score = 100
        score -= critical_count * 25  # Critical issues deduct 25 points
        score -= high_count * 10      # High priority deducts 10 points
        score -= medium_count * 5     # Medium priority deducts 5 points

        return max(0, min(100, score))
