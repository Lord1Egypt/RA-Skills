
export type Validator<T> = (data: any) => { valid: boolean; errors?: string[] };

export const isString = (val: any): boolean => typeof val === 'string';
export const isNumber = (val: any): boolean => typeof val === 'number' && !isNaN(val);
export const isBoolean = (val: any): boolean => typeof val === 'boolean';
export const isArray = (val: any): boolean => Array.isArray(val);
export const isObject = (val: any): boolean => val !== null && typeof val === 'object' && !Array.isArray(val);

export const validateObject = <T>(
    data: any, 
    fields: Record<string, Validator<any>>, 
    optionalFields: string[] = []
): { valid: boolean; errors: string[] } => {
    if (!isObject(data)) return { valid: false, errors: ['Expected object'] };
    
    const errors: string[] = [];
    
    for (const [key, validator] of Object.entries(fields)) {
        if (data[key] === undefined) {
            if (!optionalFields.includes(key)) {
                errors.push(`Missing required field: ${key}`);
            }
            continue;
        }
        
        const result = validator(data[key]);
        if (!result.valid) {
            errors.push(`Field '${key}': ${result.errors ? result.errors.join(', ') : 'Invalid'}`);
        }
    }
    
    return { valid: errors.length === 0, errors };
};

export const validateArray = <T>(
    data: any, 
    itemValidator: Validator<T>
): { valid: boolean; errors: string[] } => {
    if (!isArray(data)) return { valid: false, errors: ['Expected array'] };
    
    const errors: string[] = [];
    data.forEach((item: any, index: number) => {
        const result = itemValidator(item);
        if (!result.valid) {
            errors.push(`Item ${index}: ${result.errors ? result.errors.join(', ') : 'Invalid'}`);
        }
    });
    
    return { valid: errors.length === 0, errors };
};

export const validateEnum = <T>(values: T[]): Validator<T> => {
    return (data: any) => {
        if (values.includes(data)) return { valid: true };
        return { valid: false, errors: [`Expected one of: ${values.join(', ')}`] };
    };
};

export const validateSMFVector = (data: any): { valid: boolean; errors?: string[] } => {
    if (!isArray(data)) return { valid: false, errors: ['Expected array for SMFVector'] };
    if (data.length !== 16) return { valid: false, errors: [`Expected 16 dimensions, got ${data.length}`] };
    if (!data.every(isNumber)) return { valid: false, errors: ['All elements must be numbers'] };
    return { valid: true };
};
