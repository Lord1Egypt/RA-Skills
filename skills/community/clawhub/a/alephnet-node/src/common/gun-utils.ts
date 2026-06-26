/**
 * Gun.js Utilities
 * 
 * Helper functions for interacting with Gun.js, particularly handling
 * data types that Gun doesn't support natively (like Arrays).
 */

/**
 * Recursively converts all arrays in an object to Gun-compatible indexed objects.
 * The marker `_isArray: true` allows reconstruction on retrieval.
 */
export function arraysToGunObjects(data: any): any {
  if (data === null || data === undefined) {
    return data;
  }

  if (Array.isArray(data)) {
    const obj: Record<string, any> = { _isArray: true };
    data.forEach((item, index) => {
      obj[index.toString()] = arraysToGunObjects(item);
    });
    return obj;
  }

  if (typeof data === 'object' && !(data instanceof Date)) {
    const result: Record<string, any> = {};
    for (const key of Object.keys(data)) {
      result[key] = arraysToGunObjects(data[key]);
    }
    return result;
  }

  return data;
}

/**
 * Recursively converts Gun indexed objects (marked with `_isArray: true`) back to arrays.
 * Also handles Gun's internal metadata keys (underscore-prefixed like `_`).
 */
export function gunObjectsToArrays(data: any): any {
  if (data === null || data === undefined) {
    return data;
  }

  if (typeof data !== 'object' || data instanceof Date) {
    return data;
  }

  // Check if this object was originally an array
  if (data._isArray === true) {
    const arr: any[] = [];
    const keys = Object.keys(data)
      .filter(k => k !== '_isArray' && k !== '_' && !isNaN(parseInt(k, 10)))
      .sort((a, b) => parseInt(a, 10) - parseInt(b, 10));
    
    for (const key of keys) {
      arr.push(gunObjectsToArrays(data[key]));
    }
    return arr;
  }

  // Regular object - recurse into properties, skipping Gun metadata
  const result: Record<string, any> = {};
  for (const key of Object.keys(data)) {
    if (key === '_') continue; // Skip Gun internal metadata
    result[key] = gunObjectsToArrays(data[key]);
  }
  return result;
}
