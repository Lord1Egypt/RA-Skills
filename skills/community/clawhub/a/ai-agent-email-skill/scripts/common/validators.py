from .errors import SkillError, IMAP_SEARCH_COMMANDS


def validate_imap_query(query: str) -> str:
    """
    Validate IMAP search query against injection attacks.
    
    Args:
        query: The IMAP search query string to validate
        
    Returns:
        The validated query string
        
    Raises:
        SkillError: If the query contains invalid or dangerous commands
    """
    if not query or not query.strip():
        return "UNSEEN"
    
    query = query.strip()
    
    # Check for dangerous characters at the query level first
    # Parentheses, quotes, and semicolons can be used for injection attacks
    if any(char in query for char in "()\";"):
        raise SkillError(
            "VALIDATION_ERROR",
            "Invalid characters in search query: parentheses, quotes, and semicolons are not allowed",
            {"query": query}
        )
    
    tokens = query.upper().split()
    
    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        # Skip allowed base commands
        if token in IMAP_SEARCH_COMMANDS:
            # Commands that take an argument
            if token in ("FROM", "TO", "CC", "BCC", "SUBJECT", "BODY", "TEXT", "KEYWORD", "UNKEYWORD"):
                # Skip the next token (the argument value)
                i += 2
                continue
            if token in ("ON", "BEFORE", "AFTER", "SINCE", "SENTON", "SENTBEFORE", "SENTAFTER", "SENTSINCE"):
                # Skip the next token (the date)
                i += 2
                continue
            if token in ("HEADER",):
                # Skip the next two tokens (header name and value)
                i += 3
                continue
            if token == "NOT":
                # NOT takes one following criterion
                i += 1
                continue
            if token == "OR":
                # OR takes two following criteria
                i += 1
                continue
            if token == "LARGER" or token == "SMALLER":
                # Skip the next token (the size number)
                i += 2
                continue
            # Simple flag commands - just advance
            i += 1
            continue
        
        raise SkillError(
            "VALIDATION_ERROR",
            f"Invalid search command: {token}",
            {"token": token, "allowed_commands": sorted(list(IMAP_SEARCH_COMMANDS))[:10]}
        )
    
    return query


def validate_folder_name(name: str) -> str:
    """
    Validate folder/mailbox name against injection attacks.
    
    Args:
        name: The folder name to validate
        
    Returns:
        The validated folder name
        
    Raises:
        SkillError: If the folder name contains invalid or dangerous characters
    """
    if not name or not name.strip():
        raise SkillError(
            "VALIDATION_ERROR",
            "Folder name cannot be empty"
        )
    
    name = name.strip()
    
    # Check for control characters (0x00-0x1F)
    for i, char in enumerate(name):
        if ord(char) < 0x20:
            raise SkillError(
                "VALIDATION_ERROR",
                f"Folder name contains invalid control character at position {i}",
                {"folder_name": name, "position": i, "char_code": ord(char)}
            )
    
    # Check for dangerous characters that could indicate IMAP injection
    # IMAP uses double quotes for strings and backslash for special flags
    dangerous_chars = ['"', "\\", "*", "%"]
    for char in dangerous_chars:
        if char in name:
            raise SkillError(
                "VALIDATION_ERROR",
                f"Folder name contains invalid character: {repr(char)}",
                {"folder_name": name}
            )
    
    # Check for path traversal attempts
    if ".." in name or "/" in name:
        raise SkillError(
            "VALIDATION_ERROR",
            "Folder name cannot contain path separators",
            {"folder_name": name}
        )
    
    # Check for names that conflict with IMAP special mailboxes
    # These are allowed but should be used with caution
    reserved_names = {"INBOX", "TRASH", "SENT", "DRAFTS", "SPAM", "JUNK", "ARCHIVE"}
    if name.upper() in reserved_names:
        # Allow but this is intentional - these are common folder names
        pass
    
    # Length check - RFC 3501 recommends 255 chars max, but we use 100 for safety
    if len(name) > 100:
        raise SkillError(
            "VALIDATION_ERROR",
            "Folder name too long (max 100 characters)",
            {"length": len(name)}
        )
    
    return name
