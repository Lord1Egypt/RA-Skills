class CliError extends Error {
  constructor(code, message, details) {
    super(message);
    this.name = 'CliError';
    this.code = code;
    if (details !== undefined) {
      this.details = details;
    }
  }
}

function cliError(code, message, details) {
  return new CliError(code, message, details);
}

function exitCodeForError(error) {
  switch (error?.code) {
    case 'NO_TOKEN':
    case 'CONFIG_ERROR':
      return 2;
    case 'INVALID_VALUE':
      return 3;
    case 'NOT_FOUND':
      return 4;
    case 'AMBIGUOUS':
      return 5;
    case 'HTTP_ERROR':
    case 'API_ERROR':
      return 6;
    case 'CACHE_ERROR':
      return 7;
    case 'CAPABILITY_NOT_SUPPORTED':
      return 8;
    default:
      return 1;
  }
}

module.exports = {
  CliError,
  cliError,
  exitCodeForError,
};
